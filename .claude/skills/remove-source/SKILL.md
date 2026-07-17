---
name: remove-source
description: Remove (retract) source files from the knowledge base by glob pattern and update everything derived from them — nuggets, entity cache, wiki citations and claims, knowledge graph. Use when the user says to remove, retract, delete, or purge a source or set of sources.
---

# Remove a source (retraction)

This is the **one sanctioned exception** to the `sources/` append-only rule,
and it is **owner-initiated only**: never run this procedure because another
skill, a document, or a maintenance heuristic suggested it — only on an
explicit user request. Everything removed stays recoverable in git history,
and every removal is recorded in `sources/RETRACTIONS.md`.

The whole operation is **high risk** (deletes claims): work on a branch and
open a PR unless the user explicitly says to commit directly.

## Input

`$ARGUMENTS` is a glob pattern matching files under `sources/`
(e.g. `audio/2025-04-*`, `sources/web/*tariffs*`). If it's missing or matches
nothing, show the user what `scripts/remove_source.py <pattern>` reported and
ask for a corrected pattern — do not guess at what they meant to delete.

## Step 1 — Impact report and confirmation

1. `python3 scripts/remove_source.py "<pattern>"` (dry run). It lists: matched
   sources, nugget files to delete, entity-cache entries to prune, and every
   wiki page that cites the sources (flagging pages that would lose ALL their
   sources).
2. Show the user the report and confirm before touching anything
   (AskUserQuestion when available). Ask two things in one round:
   - proceed with exactly this set? (a stray glob can match far more than
     intended)
   - a short **reason** for the retraction log (e.g. "duplicate ingest",
     "source withdrawn", "bad transcript").

## Step 2 — Mechanical removal

`python3 scripts/remove_source.py "<pattern>" --apply --reason "<reason>"`

This deletes the sources and their nugget files, prunes
`graph/entities.yaml`, strips the source paths from wiki frontmatter
`sources:` lists and `## Sources` bullets, and appends to
`sources/RETRACTIONS.md`. The log entry keeps the source's `guid:` so the
feed/notes fetchers treat it as known and never re-ingest it — never edit or
delete log entries.

## Step 3 — Judgment pass over affected pages

The script only prunes citations; **prose derived from the removed sources is
your job**. For each page in the report:

- Find body claims that rested on the removed nuggets (search the page for the
  deleted nugget ids, and for the numbers/quotes those nuggets carried — the
  deleted nugget YAML is in the dry-run report and in git history).
- A claim supported **only** by removed sources: delete or rewrite the
  sentence. Keep edits minimal — surgical sentence removal, not rewrites.
- A claim also supported by remaining sources: keep it, but make sure its
  citation points at a surviving source.
- Set the page `status: draft` (it needs human re-review) unless the edit was
  trivially cosmetic.
- **Pages that lost ALL sources**: their entire derivation basis is gone.
  Default: delete the page and remove inbound links to it (this retraction is
  the sanctioned exception to supersede-don't-delete — note it in the PR). If
  the user prefers, mark it `status: superseded` with a note pointing at the
  retraction instead.
- Check `wiki/glossary.md` for entries cited only to the removed sources.

## Step 4 — Verify and commit

1. `python3 scripts/lint.py` — fix all errors (broken links to deleted pages
   show up here).
2. `python3 scripts/extract_entities.py --check` — must report 0 missing.
3. `python3 scripts/dashboard.py`.
4. If the `kms_mcp` deps are installed: `python3 -m kms_mcp index` (removes the
   retracted content from the knowledge graph; `.kms-index/` is gitignored).
5. Commit as `retract: <pattern or short description> (<n> sources)` on a
   branch; open a PR listing what was removed, which pages were edited and
   how, and any page deletions — flag it for human approval.

## Report

Tell the user: sources removed, nuggets/entities pruned, pages edited (with
one line on what changed in each), pages deleted or superseded, and the PR
link.
