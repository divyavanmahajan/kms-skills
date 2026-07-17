# Claude Code project guide

This repo is a self-managing knowledge system (an "LLM wiki"): raw sources are
preserved in `sources/`, compiled knowledge lives as Markdown in `wiki/`, and
skills + scripts keep the compiled layer honest.

**Read `AGENTS.md` before making any change.** It defines the operating rules
(never edit sources, supersede don't delete, citation requirements, risk tiers,
commit conventions).

## Commands

```bash
python3 scripts/lint.py          # structural lint (run before every commit touching wiki/)
python3 scripts/lint.py --strict # warnings become errors (used in CI)
python3 scripts/dashboard.py     # regenerate wiki/dashboard.md
python3 scripts/new_page.py "Title" --type topic   # scaffold a schema-compliant page
mkdocs serve                     # preview the site locally (pip install -r requirements.txt)
```

## Skills

- `/ingest <url|file|note>` — snapshot a source and compile it into wiki pages
- `/review [page]` — semantic review of stale or flagged pages
- `/contradictions` — cross-page contradiction sweep
- `/maintain` — full weekly maintenance loop (used by scheduled CI too)

## Key paths

- `policies/` — schema, citation, source, and review policies (high-risk to edit)
- `sources/` — append-only raw material; never modify existing files
- `wiki/` — compiled pages (MkDocs docs dir); every page needs schema frontmatter
- `inbox/` — drop zone for material awaiting ingestion
