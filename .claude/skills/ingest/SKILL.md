---
name: ingest
description: Ingest a source (URL, PDF, note, file in inbox/, or code doc) into the knowledge base — snapshot it under sources/, then compile or update wiki pages with citations per the repo policies. Use when the user shares material to add, says "ingest", "add this to the wiki/KB", or drops files in inbox/.
---

# Ingest a source

Follow `AGENTS.md` at all times. Read `policies/source-policy.md`,
`policies/schema.md`, and `policies/citation-policy.md` before the first ingest
in a session.

## Input

`$ARGUMENTS` may be a URL, a file path (often in `inbox/`), or pasted text. If
empty, list the contents of `inbox/` and ingest everything there (except
`README.md`, which stays put). Audio files and `inbox/podcast-*.md` feed
entries are handled by the `ingest-audio` skill's procedure (metadata
collection + transcription) — switch to it for those inputs.

## Step 1 — Collect metadata (ask, don't guess)

Gather this for every source before writing anything:

| Field | Required | Notes |
|---|---|---|
| `url` or `origin` | yes | Where it came from — URL, or origin for files/notes ("email from X", "downloaded from Y", "own notes") |
| `title` | yes | Of the work, not the filename |
| `author` | yes | Person/organization; "unknown" only if the user confirms it |
| `published` | when known | Publication/creation date (YYYY-MM-DD, or year) |
| `type` | yes | `snapshot`, `summary-notes`, `original`, or `extract` |
| `retrieved` | auto | Today |

URLs and well-formed documents usually carry these; **dropped files and pasted
text often don't. For every required field you cannot determine from the
content itself: ASK THE USER** — use the AskUserQuestion tool when available
(batch all missing fields for all pending sources into one round), otherwise
ask in plain text and wait. Do not guess authors, dates, or origins, and do
not proceed with placeholders: provenance frontmatter is what every downstream
citation rests on. If the user genuinely doesn't know a field, record it
explicitly (`author: unknown (confirmed by owner)`) and cap dependent nuggets
at `confidence: low`.

## Step 2 — Preserve the source (append-only)

1. Pick the subfolder: `sources/web/` (URLs), `sources/docs/` (PDFs/papers),
   `sources/notes/` (the user's own notes), `sources/code/` (codebase/API docs).
2. Create `sources/<sub>/YYYY-MM-DD-<slug>.md` with the metadata from Step 1
   as frontmatter.
   - URLs: fetch the page and capture the substantive content (headings, claims,
     data). If you can only capture a summary, set `type: summary-notes`.
   - Files from `inbox/`: `git mv` them into place (add the frontmatter sidecar
     for binaries), so the inbox ends up empty.
3. NEVER modify an existing file under `sources/`. A new version of an old
   source is a new dated file.

## Step 3 — Extract nuggets

From the source, list: topics covered, entities, concrete claims (especially
numbers, versions, comparisons), and anything that contradicts existing wiki
content (`grep -ri` the key terms across `wiki/` and `nuggets/`).

Record the claims as nuggets in `nuggets/<same-slug-as-source>.yaml` following
the `nuggets` skill's procedure and `policies/nugget-policy.md` — atomic
claim + context (who/when/scope) + provenance. The nugget file is the claim
inventory the wiki pages in Step 4 are compiled from.

## Step 4 — Compile into the wiki

- **Prefer updating existing pages** over creating new ones. Only create a page
  for a genuinely new concept (`python3 scripts/new_page.py "Title" --type topic`).
- Keep edits minimal and sectioned — do not rewrite whole pages.
- Every technical claim, comparison, number, or version statement must trace to
  the new source: add it to frontmatter `sources:` and the `## Sources` section.
- New/updated pages get `status: draft` (a human hasn't reviewed yet). Set
  `confidence` honestly: `medium` max for `summary-notes` sources.
- Add glossary entries for new terms, including aliases ("also called ...").
- Link the new/updated pages from related pages and check they're reachable
  from `wiki/index.md` (directly or transitively) — no orphans.
- If the source contradicts an existing page: do NOT silently overwrite. Mark
  the affected page `status: disputed`, record both positions with citations in
  *Open questions*, and flag it in your final report.

## Step 5 — Verify and commit

1. `python3 scripts/lint.py` — fix all errors.
2. `python3 scripts/dashboard.py`.
3. Commit: `ingest: <short description of source and pages touched>`.
   New pages/claims are **medium risk** — commit on a branch and open a PR
   unless the user asked you to commit directly.

## Report

Tell the user: what was preserved where, which pages were created/updated,
any contradictions found, and what needs human review.
