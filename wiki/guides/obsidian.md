---
title: Maintaining the KMS with Obsidian
status: draft
confidence: medium
created: 2026-07-17
review_after: 2026-10-15
review_interval_days: 90
sources: []
tags: [guide, obsidian, tooling]
---

# Maintaining the KMS with Obsidian

## Summary

The wiki is plain Markdown (guideline G2 in the
[maintenance guidelines](maintenance-guidelines.md)), so Obsidian works as a
manual-editing front end with zero changes to the system: open the repo as a
vault, keep links in standard Markdown format, and let Git/CI remain the
review layer. This page covers setup, the settings that keep Obsidian
compatible with `lint.py` and MkDocs, and the manual editing workflow.

## Setup

1. Clone the repo locally and open the **repo root** as a vault
   (*Open folder as vault*). Using the root — not `wiki/` — keeps `sources/`
   readable for verification while you edit.
2. Settings → **Files and links**:
   - **Use [[Wikilinks]] → OFF** — the system requires standard
     `[text](relative/path.md)` links; wikilinks break `lint.py` and MkDocs.
   - **New link format → Relative path to file** — matches how existing pages
     link.
   - **Automatically update internal links → ON** — then renames won't orphan
     links (renames are still medium-risk changes; prefer not renaming).
   - **Default location for new notes** → `wiki/topics`.
3. Settings → **Files and links → Excluded files**: add `site/`, `.claude/`,
   `scripts/` so search and graph show knowledge, not machinery.
4. `.obsidian/` is gitignored — your workspace config stays local.

## Recommended plugins

- **Obsidian Git** (community) — pull on startup, commit/push from inside
  Obsidian. Set a manual commit flow (not auto-backup) so you can write proper
  commit messages with the repo's prefixes (`review:`, `lint:`, …).
- **Dataview** (community) — live queries over page frontmatter; this gives
  you the dashboard's stale-page view inside Obsidian:

  ```text
  TABLE status, confidence, review_after
  FROM "wiki"
  WHERE review_after AND date(review_after) < date(today)
  SORT review_after ASC
  ```

- **Templates** (core) — point the template folder at `templates/` and use
  `templates/topic-page.md` when creating pages by hand (it mirrors
  `scripts/new_page.py` output).

Obsidian's built-in **Properties** panel edits the YAML frontmatter safely,
and **Graph view** is a free structure-drift monitor: orphan pages appear as
disconnected dots (color-code by path to separate `wiki/` from `sources/`).

## Manual editing workflow

Humans have more authority than agents, but the same discipline applies —
`AGENTS.md` is written for you too:

1. **Pull first** (Obsidian Git: *Pull*) — the weekly automation may have
   committed since your last edit.
2. Edit `wiki/` pages only. **Never edit `sources/`** — if a source is wrong,
   ingest a corrected version as a new dated file.
3. When you edit claims, keep citations honest: update the page's `sources:`
   list and *Sources* section (guideline G7). If you verified the page against
   its sources, you may set `status: reviewed`, update `reviewed:` to today,
   and push `review_after` forward one interval — you are the human reviewer.
4. Keep the frontmatter schema intact (`policies/schema.md`); the Properties
   panel prevents most YAML breakage.
5. Retire pages by superseding (`status: superseded` + `superseded_by:`),
   never by deleting.
6. Commit with the standard prefixes; push. CI runs `lint.py` on your push —
   if it fails, the Actions tab shows exactly which rule you broke. To check
   before pushing: `python3 scripts/lint.py` in a terminal.
7. Leave `wiki/dashboard.md` alone — it's generated; the weekly job (or
   `python3 scripts/dashboard.py`) refreshes it.

## Division of labor

Obsidian is for **reading, verifying, and hand-editing** — the human half of
the loop (guideline G8). Ingestion, nugget extraction, staleness reviews, and
contradiction sweeps stay with the skills/automation; nothing in Obsidian
depends on them, and nothing they do depends on Obsidian. Both sides meet in
Git.

## Open questions

- Obsidian on mobile + Obsidian Git works but sync conflicts with the weekly
  automation are untested here; a safer mobile flow is reading via the
  published site and editing on desktop.

## Sources

Procedural guidance by the repo owner/maintainers (unsourced per
`policies/citation-policy.md` — structural/navigation content). Obsidian
behavior claims reflect Obsidian as of mid-2026; re-verify on review.
