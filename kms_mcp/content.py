"""Parse the repo's content layers into plain dicts for indexing."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from .config import ENTITIES_FILE, NUGGETS_DIR, REPO_ROOT, SOURCES_DIR, WIKI_DIR

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$", re.MULTILINE)


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(v) for v in value]


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter dict, body) for a markdown file."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), text[match.end():]


@dataclass
class Nugget:
    uid: str          # "<file stem>#<nugget id>"
    nugget_id: str
    source: str       # repo-relative source path
    claim: str
    context: str
    confidence: str
    status: str
    tags: list[str]
    supersedes: Optional[str]
    entities: list[dict] = field(default_factory=list)

    @property
    def embed_text(self) -> str:
        return f"{self.claim}\n{self.context}".strip()


def load_nuggets() -> list[Nugget]:
    entities = load_entities()
    nuggets: list[Nugget] = []
    for path in sorted(NUGGETS_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        source = str(data.get("source", ""))
        for item in data.get("nuggets") or []:
            if not isinstance(item, dict) or "id" not in item:
                continue
            uid = f"{path.stem}#{item['id']}"
            nuggets.append(Nugget(
                uid=uid,
                nugget_id=str(item["id"]),
                source=source,
                claim=str(item.get("claim", "")).strip(),
                context=str(item.get("context", "")).strip(),
                confidence=str(item.get("confidence", "")),
                status=str(item.get("status", "active")),
                tags=_as_list(item.get("tags")),
                supersedes=item.get("supersedes"),
                entities=entities.get(uid, []),
            ))
    return nuggets


@dataclass
class Section:
    sid: str          # "<page path>#<anchor>"
    page: str
    heading: str
    text: str

    @property
    def embed_text(self) -> str:
        return f"{self.heading}\n{self.text}".strip()


@dataclass
class Page:
    path: str
    title: str
    kind: str         # topic | decision | guide | meta
    status: str
    confidence: str
    created: str
    review_after: str
    tags: list[str]
    sources: list[str]
    superseded_by: Optional[str]
    body: str
    sections: list[Section] = field(default_factory=list)


def _page_kind(rel_path: str) -> str:
    if rel_path.startswith("wiki/topics/"):
        return "topic"
    if rel_path.startswith("wiki/decisions/"):
        return "decision"
    if rel_path.startswith("wiki/guides/"):
        return "guide"
    return "meta"


def _split_sections(rel_path: str, body: str) -> list[Section]:
    """Split a page body into sections at #/##/### headings."""
    sections: list[Section] = []
    matches = list(HEADING_RE.finditer(body))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        text = body[m.end():end].strip()
        if not text:
            continue
        anchor = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
        sections.append(Section(
            sid=f"{rel_path}#{anchor}",
            page=rel_path,
            heading=m.group(2).strip(),
            text=text,
        ))
    if not sections and body.strip():
        sections.append(Section(sid=f"{rel_path}#body", page=rel_path,
                                heading="", text=body.strip()))
    return sections


def load_pages() -> list[Page]:
    pages: list[Page] = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        rel_path = _rel(path)
        if path.name == "dashboard.md":  # generated, skip
            continue
        meta, body = parse_frontmatter(path)
        pages.append(Page(
            path=rel_path,
            title=str(meta.get("title", path.stem)),
            kind=_page_kind(rel_path),
            status=str(meta.get("status", "")),
            confidence=str(meta.get("confidence", "")),
            created=str(meta.get("created", "")),
            review_after=str(meta.get("review_after", "")),
            tags=_as_list(meta.get("tags")),
            sources=_as_list(meta.get("sources")),
            superseded_by=meta.get("superseded_by"),
            body=body,
            sections=_split_sections(rel_path, body),
        ))
    return pages


@dataclass
class Source:
    path: str
    title: str
    stype: str
    published: str
    url: str
    show: str
    tags: list[str]
    description: str

    @property
    def embed_text(self) -> str:
        return f"{self.title}\n{self.description}".strip()


def load_sources() -> list[Source]:
    sources: list[Source] = []
    for path in sorted(SOURCES_DIR.rglob("*.md")):
        meta, _body = parse_frontmatter(path)
        sources.append(Source(
            path=_rel(path),
            title=str(meta.get("title", path.stem)),
            stype=str(meta.get("type", "")),
            published=str(meta.get("published", "")),
            url=str(meta.get("url", "")),
            show=str(meta.get("show", "")),
            tags=_as_list(meta.get("tags")),
            description=str(meta.get("description", "")),
        ))
    return sources


def load_entities() -> dict[str, list[dict]]:
    """Nugget uid -> [{name, type}] from the committed extraction cache."""
    if not ENTITIES_FILE.is_file():
        return {}
    try:
        data = yaml.safe_load(ENTITIES_FILE.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    result: dict[str, list[dict]] = {}
    for uid, ents in data.items():
        cleaned = []
        for e in ents or []:
            if isinstance(e, dict) and e.get("name"):
                cleaned.append({"name": str(e["name"]).strip(),
                                "type": str(e.get("type", "other")).strip()})
        result[str(uid)] = cleaned
    return result
