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
python3 scripts/fetch_feed.py                      # pull new podcast episodes into inbox/
python3 scripts/fetch_notes.py                     # sync notes from GitHub repos into inbox/
python3 scripts/build_browse.py  # generate the site's Sources + Nuggets browser (run before mkdocs)
mkdocs serve                     # preview the site locally (pip install -r requirements.txt)
```

## Skills

- `/ingest <url|file|note>` — snapshot a source, extract nuggets, compile wiki pages
- `/ingest-audio <file|episode>` — audio/podcast ingest: collects metadata (asks
  for anything missing), transcribes, then runs the normal pipeline
- `/nuggets [source]` — extract claim-level nuggets from a source into `nuggets/`
- `/review [page]` — semantic review of stale or flagged pages
- `/contradictions` — contradiction sweep over the nugget inventory + pages
- `/maintain` — full weekly maintenance loop (used by scheduled CI too)

## Key paths

- `policies/` — schema, citation, source, and review policies (high-risk to edit)
- `sources/` — append-only raw material; never modify existing files
- `nuggets/` — claim inventory (one YAML per source); claims immutable, supersede to correct
- `wiki/` — compiled pages (MkDocs docs dir); every page needs schema frontmatter
- `inbox/` — drop zone for material awaiting ingestion
