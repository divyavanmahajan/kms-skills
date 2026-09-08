# Copilot instructions for kms-skills

This repo is a compiled knowledge system: raw sources in `sources/`
(append-only), claim inventory in `nuggets/`, compiled wiki in `wiki/`, entity
cache in `graph/entities.yaml`, and a knowledge-graph MCP server in `kms_mcp/`.

**Read and follow `AGENTS.md`** — it defines the operating rules: never edit
`sources/` (retraction via the `remove-source` procedure is the only
exception), supersede don't delete, every claim needs provenance, small diffs,
risk tiers, and commit-message prefixes.

Key practices:

- Prefer the `kms` MCP tools (`kms_semantic_search`, `kms_graph_query`,
  `kms_related`, `kms_get_document`) over text search when answering questions
  from the knowledge base. The server is registered in `.vscode/mcp.json`.
- Before any commit touching `wiki/`: run `python scripts/lint.py` and fix
  errors. After changing nuggets/wiki/sources: keep `graph/entities.yaml`
  covered (`python scripts/extract_entities.py --check`) and rebuild the index
  (`python -m kms_mcp index`).
- The judgment workflows (ingest, review, contradictions, maintenance,
  retraction) are documented as procedures in `.claude/skills/*/SKILL.md` —
  follow the relevant one step by step when asked to do that kind of work.
- **No AI attribution in commits or PRs**: do not add `Co-Authored-By:` AI
  trailers, "Generated with ..." lines, model names, or session links to
  commit messages, PR titles, or PR descriptions.
- If you add or change a user-facing feature (skill, script, MCP tool, setup
  step), update both walkthroughs in the same change:
  `wiki/guides/windows-github-copilot.md` and `wiki/guides/mac-claude-code.md`.
