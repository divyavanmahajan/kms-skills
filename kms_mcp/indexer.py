"""Build the Kuzu knowledge graph + embedding index under .kms-index/.

Graph schema
------------
Nodes:
  Source(path PK, title, stype, published, url, show, description, embedding)
  Nugget(uid PK, nugget_id, claim, context, confidence, status, embedding)
  Page(path PK, title, kind, status, confidence, created, review_after)
  Section(sid PK, heading, text, embedding)
  Tag(name PK)
  Entity(name PK, etype)
Relationships:
  HAS_NUGGET(Source->Nugget)      source a nugget was extracted from
  CITES(Page->Source)             page frontmatter `sources:` list
  HAS_SECTION(Page->Section)      page body split at headings
  MENTIONS(Nugget->Entity)        LLM-extracted named entities
  NUGGET_TAG / PAGE_TAG / SOURCE_TAG (-> Tag)
  SUPERSEDES(Nugget->Nugget)      newer claim corrects an older one
  PAGE_SUPERSEDES(Page->Page)     successor page -> superseded page
"""

import json
import shutil
from datetime import datetime, timezone

import kuzu

from . import content
from .config import DB_FILE, INDEX_DIR, MANIFEST_FILE, EMBEDDING_MODEL, content_hash
from .embeddings import embed_texts

SCHEMA = [
    "CREATE NODE TABLE Source(path STRING PRIMARY KEY, title STRING, stype STRING, "
    "published STRING, url STRING, show STRING, description STRING, embedding FLOAT[384])",
    "CREATE NODE TABLE Nugget(uid STRING PRIMARY KEY, nugget_id STRING, claim STRING, "
    "context STRING, confidence STRING, status STRING, embedding FLOAT[384])",
    "CREATE NODE TABLE Page(path STRING PRIMARY KEY, title STRING, kind STRING, "
    "status STRING, confidence STRING, created STRING, review_after STRING)",
    "CREATE NODE TABLE Section(sid STRING PRIMARY KEY, heading STRING, text STRING, "
    "embedding FLOAT[384])",
    "CREATE NODE TABLE Tag(name STRING PRIMARY KEY)",
    "CREATE NODE TABLE Entity(name STRING PRIMARY KEY, etype STRING)",
    "CREATE REL TABLE HAS_NUGGET(FROM Source TO Nugget)",
    "CREATE REL TABLE CITES(FROM Page TO Source)",
    "CREATE REL TABLE HAS_SECTION(FROM Page TO Section)",
    "CREATE REL TABLE MENTIONS(FROM Nugget TO Entity)",
    "CREATE REL TABLE NUGGET_TAG(FROM Nugget TO Tag)",
    "CREATE REL TABLE PAGE_TAG(FROM Page TO Tag)",
    "CREATE REL TABLE SOURCE_TAG(FROM Source TO Tag)",
    "CREATE REL TABLE SUPERSEDES(FROM Nugget TO Nugget)",
    "CREATE REL TABLE PAGE_SUPERSEDES(FROM Page TO Page)",
]


def build_index(verbose: bool = True) -> dict:
    """(Re)build the whole index. Returns the manifest dict."""
    def say(msg: str) -> None:
        if verbose:
            print(msg, flush=True)

    INDEX_DIR.mkdir(exist_ok=True)
    for stale in (DB_FILE, DB_FILE.with_suffix(".kuzu.wal")):
        if stale.is_file():
            stale.unlink()
        elif stale.is_dir():
            shutil.rmtree(stale)

    say("Loading content...")
    nuggets = content.load_nuggets()
    pages = content.load_pages()
    sources = content.load_sources()
    sections = [s for p in pages for s in p.sections]

    say(f"Embedding {len(nuggets)} nuggets, {len(sections)} sections, "
        f"{len(sources)} sources...")
    nug_vecs = embed_texts([n.embed_text for n in nuggets]) if nuggets else []
    sec_vecs = embed_texts([s.embed_text for s in sections]) if sections else []
    src_vecs = embed_texts([s.embed_text for s in sources]) if sources else []

    db = kuzu.Database(str(DB_FILE))
    conn = kuzu.Connection(db)
    for ddl in SCHEMA:
        conn.execute(ddl)

    say("Inserting nodes...")
    source_paths = {s.path for s in sources}
    for src, vec in zip(sources, src_vecs):
        conn.execute(
            "CREATE (:Source {path:$path, title:$title, stype:$stype, published:$published, "
            "url:$url, show:$show, description:$description, embedding:$embedding})",
            {"path": src.path, "title": src.title, "stype": src.stype,
             "published": src.published, "url": src.url, "show": src.show,
             "description": src.description, "embedding": vec.tolist()})
    # Placeholder Source nodes for referenced-but-missing paths, so edges resolve.
    referenced = {n.source for n in nuggets if n.source} | \
                 {sp for p in pages for sp in p.sources}
    for path in sorted(referenced - source_paths):
        conn.execute(
            "CREATE (:Source {path:$path, title:$path, stype:'missing'})",
            {"path": path})
        source_paths.add(path)

    for nug, vec in zip(nuggets, nug_vecs):
        conn.execute(
            "CREATE (:Nugget {uid:$uid, nugget_id:$nugget_id, claim:$claim, context:$context, "
            "confidence:$confidence, status:$status, embedding:$embedding})",
            {"uid": nug.uid, "nugget_id": nug.nugget_id, "claim": nug.claim,
             "context": nug.context, "confidence": nug.confidence,
             "status": nug.status, "embedding": vec.tolist()})

    for page in pages:
        conn.execute(
            "CREATE (:Page {path:$path, title:$title, kind:$kind, status:$status, "
            "confidence:$confidence, created:$created, review_after:$review_after})",
            {"path": page.path, "title": page.title, "kind": page.kind,
             "status": page.status, "confidence": page.confidence,
             "created": page.created, "review_after": page.review_after})

    for sec, vec in zip(sections, sec_vecs):
        conn.execute(
            "CREATE (:Section {sid:$sid, heading:$heading, text:$text, embedding:$embedding})",
            {"sid": sec.sid, "heading": sec.heading, "text": sec.text,
             "embedding": vec.tolist()})

    tags = {t for n in nuggets for t in n.tags} | \
           {t for p in pages for t in p.tags} | \
           {t for s in sources for t in s.tags}
    for tag in sorted(tags):
        conn.execute("CREATE (:Tag {name:$name})", {"name": tag})

    entities: dict[str, str] = {}
    for nug in nuggets:
        for ent in nug.entities:
            entities.setdefault(ent["name"], ent["type"])
    for name, etype in sorted(entities.items()):
        conn.execute("CREATE (:Entity {name:$name, etype:$etype})",
                     {"name": name, "etype": etype})

    say("Inserting relationships...")
    nugget_uids = {n.uid for n in nuggets}
    counts = {"HAS_NUGGET": 0, "CITES": 0, "HAS_SECTION": 0, "MENTIONS": 0,
              "TAGS": 0, "SUPERSEDES": 0}

    def rel(query: str, params: dict, counter: str) -> None:
        conn.execute(query, params)
        counts[counter] += 1

    for nug in nuggets:
        if nug.source in source_paths:
            rel("MATCH (s:Source {path:$s}), (n:Nugget {uid:$n}) "
                "CREATE (s)-[:HAS_NUGGET]->(n)",
                {"s": nug.source, "n": nug.uid}, "HAS_NUGGET")
        for tag in nug.tags:
            rel("MATCH (n:Nugget {uid:$n}), (t:Tag {name:$t}) CREATE (n)-[:NUGGET_TAG]->(t)",
                {"n": nug.uid, "t": tag}, "TAGS")
        for ent in nug.entities:
            rel("MATCH (n:Nugget {uid:$n}), (e:Entity {name:$e}) CREATE (n)-[:MENTIONS]->(e)",
                {"n": nug.uid, "e": ent["name"]}, "MENTIONS")
        if nug.supersedes:
            target = nug.supersedes if "#" in str(nug.supersedes) \
                else f"{nug.uid.split('#')[0]}#{nug.supersedes}"
            if target in nugget_uids:
                rel("MATCH (a:Nugget {uid:$a}), (b:Nugget {uid:$b}) "
                    "CREATE (a)-[:SUPERSEDES]->(b)",
                    {"a": nug.uid, "b": target}, "SUPERSEDES")

    page_paths = {p.path for p in pages}
    for page in pages:
        for src in page.sources:
            if src in source_paths:
                rel("MATCH (p:Page {path:$p}), (s:Source {path:$s}) CREATE (p)-[:CITES]->(s)",
                    {"p": page.path, "s": src}, "CITES")
        for sec in page.sections:
            rel("MATCH (p:Page {path:$p}), (s:Section {sid:$s}) CREATE (p)-[:HAS_SECTION]->(s)",
                {"p": page.path, "s": sec.sid}, "HAS_SECTION")
        for tag in page.tags:
            rel("MATCH (p:Page {path:$p}), (t:Tag {name:$t}) CREATE (p)-[:PAGE_TAG]->(t)",
                {"p": page.path, "t": tag}, "TAGS")
        if page.superseded_by and page.superseded_by in page_paths:
            rel("MATCH (a:Page {path:$a}), (b:Page {path:$b}) "
                "CREATE (a)-[:PAGE_SUPERSEDES]->(b)",
                {"a": page.superseded_by, "b": page.path}, "SUPERSEDES")

    for src in sources:
        for tag in src.tags:
            rel("MATCH (s:Source {path:$s}), (t:Tag {name:$t}) CREATE (s)-[:SOURCE_TAG]->(t)",
                {"s": src.path, "t": tag}, "TAGS")

    conn.close()
    db.close()

    manifest = {
        "content_hash": content_hash(),
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "embedding_model": EMBEDDING_MODEL,
        "nodes": {"sources": len(sources), "nuggets": len(nuggets),
                  "pages": len(pages), "sections": len(sections),
                  "tags": len(tags), "entities": len(entities)},
        "relationships": counts,
    }
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2))
    say(f"Index built: {manifest['nodes']} / {counts}")
    return manifest


def manifest() -> dict | None:
    if MANIFEST_FILE.is_file():
        return json.loads(MANIFEST_FILE.read_text())
    return None


def is_stale() -> bool:
    m = manifest()
    return m is None or not DB_FILE.exists() or m.get("content_hash") != content_hash()
