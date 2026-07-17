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

**If the input is a directory or many similar files (a bulk ingest), read
[§ Bulk ingest](#bulk-ingest-a-directory-or-many-similar-files) FIRST** — the
steps below assume one source at a time and will lead you astray at volume.

## Bulk ingest (a directory or many similar files)

Ingesting dozens or hundreds of homogeneous files (e.g. a folder of episode
notes, an export of articles) is a different job from ingesting one source. The
same policies apply, but the *method* changes. Do this in order:

1. **Match the established pattern — don't invent one.** Before writing
   anything, look at how this repo already handles this kind of source:
   - Is there **purpose-built tooling**? Check `scripts/` (e.g.
     `fetch_notes.py`, `fetch_feed.py`) and `feeds.yaml`. If a script already
     defines the canonical frontmatter and naming for this source, **reuse its
     logic** (import its functions) rather than hand-rolling your own shape.
   - Is there **one already-ingested example** of the same source? Open it and
     copy its frontmatter fields, `type`, folder (`sources/audio/`,
     `sources/web/`, …), author/`show` conventions, and slug format **exactly**.
     One inconsistent field (wrong `type`, wrong author, wrong folder) multiplied
     across hundreds of files is a large, hard-to-review mess.
2. **A script MAY preserve sources (Step 2). A script must NOT write nuggets or
   wiki prose.** Mechanically snapshotting many files into `sources/` with the
   correct frontmatter is fine and encouraged at volume — it is faithful and
   append-only. But see the ⛔ in Step 3: nuggets and pages require *reading*,
   never pattern-matching.
3. **Dedup by `guid`/`origin`.** Skip files already present in `sources/` (the
   `known_guids()` helper in `fetch_feed.py` scans `inbox/` + `sources/`), so a
   re-run doesn't duplicate an earlier ingest.
4. **Agree the depth before doing the expensive part.** Preserving N sources is
   cheap and safe; extracting good nuggets and compiling pages for N sources is
   a large synthesis job. Ask the user (AskUserQuestion) which they want:
   *(a) themed synthesis* — preserve all sources, then compile a **small** set
   of cross-cutting themed pages (recommended); *(b) full per-source synthesis*
   — nuggets for every source (large token cost); or *(c) sources only* — stop
   after Step 2 and compile later. Commit the source-preservation step on its
   own so progress is saved regardless of the depth chosen.
5. **To read at volume, fan out subagents**, one per theme or per batch of
   files, each returning *verified* claims tagged with the **exact source
   filename**. Assemble their output into nuggets (Step 3) and pages (Step 4).
   The claims must come from an agent that actually read the file — not from a
   script scanning for numbers.

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

> ⛔ **Never auto-generate nuggets with a regex/script that scrapes numbers or
> sentences.** A nugget is a hand-written claim **plus context** that resolves
> who/when/scope — a pattern-matched line is a chunk with extra steps and
> violates `policies/nugget-policy.md`. Every nugget must come from *reading*
> the source (yourself, or a subagent that read it). At volume, read via
> fan-out subagents; a script only *assembles their verified output* into the
> YAML schema, it never invents the claims. Confidence is capped at `medium`
> for `summary-notes` sources. Keep `id`s globally unique (kebab-case); when
> the same source is cited by several themes, merge into one
> `nuggets/<slug>.yaml`.

## Step 4 — Compile into the wiki

- **Prefer FEWER, better pages.** One concept per page (see `AGENTS.md` page
  hygiene). **Never create one page per source** for a bulk ingest — a folder of
  100 episodes becomes a *handful* of cross-cutting **themed** topic pages
  (e.g. "AI agents", "AI economics"), each synthesizing many sources, NOT 100
  near-duplicate pages. Match the house style of an existing topic page.
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
