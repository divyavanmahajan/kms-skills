# kms_mcp — knowledge graph + semantic search MCP server

An MCP server that exposes this knowledge repo to agents as a **Kuzu knowledge
graph** with **local semantic search**. Claude Code sessions in this repo pick
it up automatically via `.mcp.json`; any other MCP client can connect over
stdio or streamable HTTP.

## Setup

```bash
pip install -r requirements-mcp.txt
python3 -m kms_mcp index          # build .kms-index/ (first run downloads the
                                  # ~90MB all-MiniLM-L6-v2 embedding model once)
```

That's it for Claude Code — open the repo and the `kms` MCP server is available.

Other transports:

```bash
python3 -m kms_mcp                          # stdio MCP server (what .mcp.json runs)
python3 -m kms_mcp serve --http --port 8471 # streamable HTTP at http://127.0.0.1:8471/mcp
python3 -m kms_mcp search "agent adoption"  # quick search from the terminal
```

For remote agents, run the HTTP transport somewhere reachable (bind
`--host 0.0.0.0` behind your own auth/reverse proxy — the server itself does
no authentication).

## Tools

| Tool | What it does |
|---|---|
| `kms_semantic_search` | Embedding search over nuggets (claims), wiki sections, and source titles/descriptions |
| `kms_graph_query` | Read-only Cypher against the Kuzu graph (write clauses rejected) |
| `kms_graph_schema` | Schema, node/edge counts, staleness, example queries — call before writing Cypher |
| `kms_get_document` | Full content of a page / source / nugget / section by id, with graph context |
| `kms_related` | Everything connected to a node; entity/tag lookup is fuzzy ("nvidia" works) |
| `kms_reindex` | Rebuild the index after content changes |

## The graph

```
Source ──HAS_NUGGET──▶ Nugget ──MENTIONS──▶ Entity
  ▲                      │  └──NUGGET_TAG──▶ Tag ◀──PAGE_TAG/SOURCE_TAG──
  └──────CITES────────  Page ──HAS_SECTION──▶ Section
Nugget ──SUPERSEDES──▶ Nugget      Page ──PAGE_SUPERSEDES──▶ Page
```

Everything is compiled from repo content: nodes/edges come from `nuggets/*.yaml`,
wiki frontmatter + section headings, source frontmatter, and the entity
extraction cache `graph/entities.yaml` (maintained by
`scripts/extract_entities.py`). The graph is a **derived artifact** — to change
it, edit the content and reindex; the query tool refuses writes.

Embeddings (384-dim, L2-normalised) are stored on Nugget/Section/Source nodes
in Kuzu; search is exact cosine over the whole corpus in memory — at this scale
(hundreds of items) that's faster than an ANN index and has no approximation
error.

## Index lifecycle

- The index lives in `.kms-index/` (gitignored): `kms.kuzu`, `manifest.json`,
  and the cached embedding model.
- `manifest.json` records a content hash over `nuggets/`, `wiki/`, `sources/`,
  and `graph/entities.yaml`. When repo content changes, tools include a
  staleness warning; call `kms_reindex` (or `python3 -m kms_mcp index`).
- A missing index is built automatically on first tool use.
- CI (`.github/workflows/index.yml`) rebuilds the index on pushes to `main`
  and uploads it as the `kms-index` artifact, which also verifies that the
  graph builds cleanly against the current content.

## Keeping entities fresh

Entity nodes come from `graph/entities.yaml`. After ingesting new sources:

```bash
python3 scripts/extract_entities.py --check   # which nuggets lack entities?
python3 scripts/extract_entities.py           # extract just the missing ones (needs ANTHROPIC_API_KEY)
python3 -m kms_mcp index
```

Nuggets without cache entries still get full graph + search coverage — they
just lack `MENTIONS` edges until extraction runs.
