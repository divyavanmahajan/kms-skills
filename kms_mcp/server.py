"""FastMCP server exposing the KMS knowledge graph + semantic search.

Tools (all read-only except kms_reindex):
  kms_semantic_search  embedding search over nuggets, wiki sections, sources
  kms_graph_query      read-only Cypher against the Kuzu graph
  kms_graph_schema     schema, node/edge counts, example queries, index status
  kms_get_document     full content of a page / source / nugget by id
  kms_related          graph neighborhood of any node (incl. entity lookup)
  kms_reindex          rebuild the index after content changes
"""

import json
import re
from typing import Optional

import kuzu
from mcp.server.mcpserver import MCPServer

from . import indexer
from .config import DB_FILE, REPO_ROOT, content_fingerprint
from .search import SearchIndex

mcp = MCPServer("kms_mcp")

WRITE_TOKENS = re.compile(
    r"\b(CREATE|MERGE|DELETE|DETACH|SET|DROP|ALTER|COPY|IMPORT|EXPORT|ATTACH|INSTALL|LOAD)\b",
    re.IGNORECASE)


class _State:
    """Lazily opened DB handle + search index, rebuilt on demand."""

    def __init__(self) -> None:
        self.db: Optional[kuzu.Database] = None
        self.conn: Optional[kuzu.Connection] = None
        self.index: Optional[SearchIndex] = None

    def open(self) -> None:
        if not DB_FILE.exists():
            indexer.build_index(verbose=False)
        self.db = kuzu.Database(str(DB_FILE))
        self.conn = kuzu.Connection(self.db)
        self.index = SearchIndex(self.conn)

    def ensure(self) -> kuzu.Connection:
        if self.conn is None:
            self.open()
        return self.conn

    def search_index(self) -> SearchIndex:
        self.ensure()
        return self.index

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()
        if self.db is not None:
            self.db.close()
        self.db = self.conn = self.index = None

    def rebuild(self) -> dict:
        global _stale_cache
        self.close()
        manifest = indexer.build_index(verbose=False)
        self.open()
        _stale_cache = None
        return manifest


STATE = _State()

# (content_fingerprint, is_stale) — full content hashing only reruns when a
# stat-level fingerprint of the content files changes, so tool calls stay cheap.
_stale_cache: Optional[tuple[str, bool]] = None


def _is_stale() -> bool:
    global _stale_cache
    fingerprint = content_fingerprint()
    if _stale_cache is None or _stale_cache[0] != fingerprint:
        _stale_cache = (fingerprint, indexer.is_stale())
    return _stale_cache[1]


def _staleness_note() -> dict:
    if _is_stale():
        return {"warning": "Index is stale (content changed since last build). "
                           "Call kms_reindex for up-to-date results."}
    return {}


def _sanitize(value):
    """Make Kuzu values JSON-safe and strip bulky embedding vectors."""
    if isinstance(value, dict):
        return {k: _sanitize(v) for k, v in value.items()
                if k not in ("embedding", "_id")}
    if isinstance(value, (list, tuple)):
        if len(value) >= 100 and all(isinstance(v, float) for v in value[:5]):
            return f"<embedding[{len(value)}]>"
        return [_sanitize(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _run_query(cypher: str, limit: int) -> dict:
    conn = STATE.ensure()
    result = conn.execute(cypher)
    columns = result.get_column_names()
    rows = []
    while result.has_next() and len(rows) < limit:
        rows.append([_sanitize(v) for v in result.get_next()])
    return {"columns": columns, "rows": rows, "row_count": len(rows),
            "truncated": result.has_next()}


@mcp.tool(name="kms_semantic_search",
          annotations={"title": "Semantic search over the knowledge base",
                       "readOnlyHint": True, "idempotentHint": True,
                       "openWorldHint": False})
def kms_semantic_search(query: str, limit: int = 10,
                        kinds: Optional[list[str]] = None,
                        min_score: float = 0.25) -> str:
    """Semantic (embedding) search across the knowledge base.

    Searches three kinds of items with a local sentence-embedding model:
    - "nugget": atomic claims with provenance (best for facts/statistics)
    - "section": wiki page sections (best for synthesized overviews)
    - "source": raw source documents by title/description (podcast episodes, notes)

    Args:
        query: Natural-language query, e.g. "enterprise agent deployment rates".
        limit: Max results (default 10).
        kinds: Optional filter, subset of ["nugget", "section", "source"].
        min_score: Minimum cosine similarity 0-1 (default 0.25; lower = more results).

    Returns:
        JSON: {"results": [{"id", "kind", "score", "title", "detail"}...]}.
        Use each result's "id" with kms_get_document (full content) or
        kms_related (graph context). Nugget ids look like "<file>#<claim-id>",
        sections like "wiki/page.md#anchor", sources are file paths.
    """
    hits = STATE.search_index().search(query, limit=limit, kinds=kinds,
                                       min_score=min_score)
    payload = {"results": [vars(h) for h in hits], **_staleness_note()}
    if not hits:
        payload["hint"] = ("No results above min_score. Try a lower min_score, "
                           "different phrasing, or kms_graph_query for exact matches.")
    return json.dumps(payload, indent=2)


@mcp.tool(name="kms_graph_query",
          annotations={"title": "Cypher query on the knowledge graph",
                       "readOnlyHint": True, "idempotentHint": True,
                       "openWorldHint": False})
def kms_graph_query(cypher: str, limit: int = 50) -> str:
    """Run a read-only Cypher query against the Kuzu knowledge graph.

    Call kms_graph_schema first to see node/relationship tables and example
    queries. Write operations (CREATE/SET/DELETE/...) are rejected — the graph
    is a compiled artifact; edit the repo content and kms_reindex instead.

    Args:
        cypher: A Kuzu Cypher query, e.g.
            MATCH (n:Nugget)-[:MENTIONS]->(e:Entity {name:'Nvidia'})
            RETURN n.uid, n.claim
        limit: Max rows returned (default 50).

    Returns:
        JSON: {"columns": [...], "rows": [...], "row_count": n, "truncated": bool}.
        Embedding vectors are elided from results. Errors return
        {"error": "..."} with the Kuzu message — fix the query and retry.
    """
    if WRITE_TOKENS.search(cypher):
        return json.dumps({"error": "Write operations are not allowed. This graph is "
                           "compiled from repo content; edit nuggets/wiki and run "
                           "kms_reindex instead."})
    try:
        return json.dumps({**_run_query(cypher, limit), **_staleness_note()},
                          indent=2, default=str)
    except Exception as e:  # Kuzu raises RuntimeError with a parser/binder message
        return json.dumps({"error": str(e),
                           "hint": "Check kms_graph_schema for table/property names."})


@mcp.tool(name="kms_graph_schema",
          annotations={"title": "Knowledge graph schema and status",
                       "readOnlyHint": True, "idempotentHint": True,
                       "openWorldHint": False})
def kms_graph_schema() -> str:
    """Describe the knowledge graph: schema, counts, index status, example queries.

    Call this before writing kms_graph_query Cypher.

    Returns:
        JSON with:
        - schema: node tables (with properties) and relationship tables
        - manifest: node/edge counts, build time, embedding model
        - stale: whether repo content changed since the last index build
        - examples: ready-to-run Cypher queries
    """
    STATE.ensure()
    schema = {
        "nodes": {
            "Source": "path (PK, e.g. 'sources/audio/2025-07-06-....md'), title, stype, published, url, show, description",
            "Nugget": "uid (PK, '<file>#<id>'), nugget_id, claim, context, confidence, status",
            "Page": "path (PK, e.g. 'wiki/topics/ai-agents.md'), title, kind (topic|decision|guide|meta), status, confidence, created, review_after",
            "Section": "sid (PK, '<page path>#<anchor>'), heading, text",
            "Tag": "name (PK)",
            "Entity": "name (PK), etype (company|person|model|organization|report|technology|place|event)",
        },
        "relationships": {
            "HAS_NUGGET": "Source -> Nugget (nugget extracted from source)",
            "CITES": "Page -> Source (page frontmatter citation)",
            "HAS_SECTION": "Page -> Section",
            "MENTIONS": "Nugget -> Entity (extracted named entities)",
            "NUGGET_TAG / PAGE_TAG / SOURCE_TAG": "-> Tag",
            "SUPERSEDES": "Nugget -> Nugget (newer claim corrects older)",
            "PAGE_SUPERSEDES": "Page -> Page (successor -> superseded)",
        },
    }
    examples = [
        "MATCH (e:Entity) RETURN e.etype, count(*) ORDER BY count(*) DESC",
        "MATCH (n:Nugget)-[:MENTIONS]->(e:Entity {name:'Anthropic'}) RETURN n.uid, n.claim",
        "MATCH (p:Page)-[:CITES]->(s:Source)-[:HAS_NUGGET]->(n:Nugget)-[:MENTIONS]->(e:Entity) "
        "WHERE p.path = 'wiki/topics/ai-agents.md' RETURN DISTINCT e.name, e.etype",
        "MATCH (a:Nugget)-[:SUPERSEDES]->(b:Nugget) RETURN a.uid, a.claim, b.uid",
        "MATCH (t:Tag)<-[:NUGGET_TAG]-(n:Nugget) RETURN t.name, count(n) AS uses ORDER BY uses DESC LIMIT 20",
    ]
    return json.dumps({"schema": schema, "manifest": indexer.manifest(),
                       "stale": _is_stale(), "examples": examples}, indent=2)


@mcp.tool(name="kms_get_document",
          annotations={"title": "Get full document content",
                       "readOnlyHint": True, "idempotentHint": True,
                       "openWorldHint": False})
def kms_get_document(id: str, max_chars: int = 20000, offset: int = 0) -> str:
    """Fetch full content for any id returned by other tools.

    Accepts:
    - wiki page path ("wiki/topics/ai-agents.md") -> full markdown
    - source path ("sources/audio/2025-....md") -> full markdown (may be a transcript)
    - nugget uid ("2025-07-06-...#menlo-consumer-adoption-61-tools") -> claim,
      context, tags, entities, source
    - section sid ("wiki/topics/ai-agents.md#summary") -> that section's text

    Args:
        id: Document identifier as above.
        max_chars: Truncate file content to this many characters (default 20000).
        offset: Character offset for paging through long transcripts.

    Returns:
        JSON with the content plus graph context (citations, tags, entities).
        Truncated responses include "next_offset".
    """
    conn = STATE.ensure()
    max_chars = max(1, max_chars)
    offset = max(0, offset)
    try:
        if "#" in id and not id.startswith("wiki/"):
            return json.dumps(_get_nugget(conn, id), indent=2)
        if "#" in id:
            return json.dumps(_get_section(conn, id), indent=2)
        return json.dumps(_get_file(conn, id, max_chars, offset), indent=2)
    except FileNotFoundError:
        return json.dumps({"error": f"Not found: {id}",
                           "hint": "Use ids exactly as returned by kms_semantic_search "
                                   "or kms_graph_query."})


def _get_nugget(conn, uid: str) -> dict:
    result = conn.execute(
        "MATCH (s:Source)-[:HAS_NUGGET]->(n:Nugget {uid:$uid}) "
        "RETURN n.claim, n.context, n.confidence, n.status, s.path, s.title, s.url",
        {"uid": uid})
    if not result.has_next():
        raise FileNotFoundError(uid)
    claim, context, confidence, status, spath, stitle, surl = result.get_next()
    tags = [r[0] for r in _iter(conn.execute(
        "MATCH (n:Nugget {uid:$uid})-[:NUGGET_TAG]->(t:Tag) RETURN t.name", {"uid": uid}))]
    ents = [{"name": r[0], "type": r[1]} for r in _iter(conn.execute(
        "MATCH (n:Nugget {uid:$uid})-[:MENTIONS]->(e:Entity) RETURN e.name, e.etype",
        {"uid": uid}))]
    return {"kind": "nugget", "uid": uid, "claim": claim, "context": context,
            "confidence": confidence, "status": status, "tags": tags,
            "entities": ents,
            "source": {"path": spath, "title": stitle, "url": surl}}


def _get_section(conn, sid: str) -> dict:
    result = conn.execute(
        "MATCH (p:Page)-[:HAS_SECTION]->(s:Section {sid:$sid}) "
        "RETURN s.heading, s.text, p.path, p.title", {"sid": sid})
    if not result.has_next():
        raise FileNotFoundError(sid)
    heading, text, path, title = result.get_next()
    return {"kind": "section", "sid": sid, "heading": heading, "text": text,
            "page": {"path": path, "title": title}}


def _get_file(conn, rel_path: str, max_chars: int, offset: int) -> dict:
    path = (REPO_ROOT / rel_path).resolve()
    if not path.is_relative_to(REPO_ROOT) or not path.is_file():
        raise FileNotFoundError(rel_path)
    text = path.read_text(encoding="utf-8")
    chunk = text[offset:offset + max_chars]
    payload = {"kind": "page" if rel_path.startswith("wiki/") else "source",
               "path": rel_path, "length": len(text), "offset": offset,
               "content": chunk}
    if offset + len(chunk) < len(text):
        payload["next_offset"] = offset + len(chunk)
    if rel_path.startswith("wiki/"):
        payload["cites"] = [r[0] for r in _iter(conn.execute(
            "MATCH (p:Page {path:$p})-[:CITES]->(s:Source) RETURN s.path",
            {"p": rel_path}))]
    else:
        payload["nugget_uids"] = [r[0] for r in _iter(conn.execute(
            "MATCH (s:Source {path:$p})-[:HAS_NUGGET]->(n:Nugget) RETURN n.uid",
            {"p": rel_path}))]
    return payload


@mcp.tool(name="kms_related",
          annotations={"title": "Graph neighborhood of a node",
                       "readOnlyHint": True, "idempotentHint": True,
                       "openWorldHint": False})
def kms_related(id: str, limit: int = 40) -> str:
    """List everything directly connected to a node in the knowledge graph.

    Accepts a nugget uid, page path, source path, tag name, or entity name
    (entity/tag matching is case-insensitive substring, so "nvidia" works).
    Great for "show me everything about X" and for hopping from a search hit
    to its provenance and related material.

    Args:
        id: Node identifier or entity/tag name.
        limit: Max neighbors per relationship direction (default 40).

    Returns:
        JSON: {"node": {...}, "neighbors": [{"relationship", "direction",
        "label", "id", "title"}...]}. Neighbor ids feed back into
        kms_get_document / kms_related.
    """
    conn = STATE.ensure()
    node = _find_node(conn, id)
    if node is None:
        return json.dumps({"error": f"No node found for '{id}'",
                           "hint": "Pass a nugget uid, page/source path, or "
                                   "entity/tag name (substring ok)."})
    label, key_prop, key = node
    neighbors = []
    result = conn.execute(
        f"MATCH (a:{label} {{{key_prop}:$key}})-[r]->(b) "
        f"RETURN label(r), label(b), b, false AS incoming LIMIT $lim",
        {"key": key, "lim": limit})
    for row in _iter(result):
        neighbors.append(_neighbor(row))
    result = conn.execute(
        f"MATCH (a:{label} {{{key_prop}:$key}})<-[r]-(b) "
        f"RETURN label(r), label(b), b, true AS incoming LIMIT $lim",
        {"key": key, "lim": limit})
    for row in _iter(result):
        neighbors.append(_neighbor(row))
    return json.dumps({"node": {"label": label, key_prop: key},
                       "neighbors": neighbors, **_staleness_note()}, indent=2)


def _neighbor(row) -> dict:
    rel_label, node_label, props, incoming = row
    props = _sanitize(props)
    id_val = props.get("uid") or props.get("path") or props.get("sid") or props.get("name")
    title = (props.get("claim") or props.get("title") or props.get("heading")
             or props.get("name") or "")
    out = {"relationship": rel_label, "direction": "in" if incoming else "out",
           "label": node_label, "id": id_val, "title": (title or "")[:200]}
    if props.get("etype"):
        out["etype"] = props["etype"]
    return out


def _find_node(conn, id: str):
    """Resolve an id to (label, key_property, key_value)."""
    exact = [("Nugget", "uid"), ("Page", "path"), ("Source", "path"),
             ("Section", "sid"), ("Entity", "name"), ("Tag", "name")]
    for label, prop in exact:
        result = conn.execute(
            f"MATCH (n:{label}) WHERE n.{prop} = $id RETURN n.{prop} LIMIT 1",
            {"id": id})
        if result.has_next():
            return label, prop, result.get_next()[0]
    for label, prop in (("Entity", "name"), ("Tag", "name")):
        result = conn.execute(
            f"MATCH (n:{label}) WHERE lower(n.{prop}) CONTAINS lower($id) "
            f"RETURN n.{prop} LIMIT 1", {"id": id})
        if result.has_next():
            return label, prop, result.get_next()[0]
    return None


@mcp.tool(name="kms_reindex",
          annotations={"title": "Rebuild the knowledge graph index",
                       "readOnlyHint": False, "destructiveHint": False,
                       "idempotentHint": True, "openWorldHint": False})
def kms_reindex() -> str:
    """Rebuild the Kuzu graph and embeddings from current repo content.

    Run after editing nuggets/, wiki/, sources/, or graph/entities.yaml
    (other tools will warn when the index is stale). Takes ~10-60s.
    Only touches the gitignored .kms-index/ directory — repo content is
    never modified.

    Returns:
        JSON manifest: content hash, build time, node/relationship counts.
    """
    return json.dumps(STATE.rebuild(), indent=2)


def _iter(result):
    while result.has_next():
        yield result.get_next()
