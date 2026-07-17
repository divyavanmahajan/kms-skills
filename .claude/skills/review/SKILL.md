---
name: review
description: Semantic review of wiki pages — verify claims still match cited sources, detect source/citation/terminology/decision drift, then bump review dates or mark pages disputed/superseded. Use for stale pages flagged by the dashboard, before promoting a draft to reviewed, or when the user asks to "review the wiki".
---

# Semantic review

Follow `AGENTS.md`. This skill checks **truth and freshness**; `scripts/lint.py`
already covers structure — run it, don't re-do it by hand.

## Input

`$ARGUMENTS` may name specific pages. If empty: regenerate the dashboard
(`python3 scripts/dashboard.py`), then review the stale pages ("Pages needing
review"), oldest due-date first. Limit to ~5 pages per session so diffs stay
reviewable.

## Per-page procedure (see policies/review-policy.md)

1. **Read the page and every file in its `sources:` list.**
2. **Citation drift** — for each concrete claim, confirm a listed source still
   supports it. Unsupported claims move to *Open questions* (never silently
   deleted) and drop the page's `confidence`.
3. **Source drift** — could the underlying facts have changed (tool versions,
   pricing, APIs)? If the page makes version/pricing claims and the source is
   older than the page's `review_interval_days`, re-check reality (fetch the
   current page/docs if network is available; otherwise flag for re-ingestion).
4. **Terminology drift** — do the page's terms match `wiki/glossary.md`? Add
   aliases to the glossary rather than renaming historical content.
5. **Decision drift** — if the page states a practice that a
   `wiki/decisions/` record has superseded, update the reference.

## Outcomes (pick one per page)

- **Still accurate** → set `reviewed: <today>`, bump
  `review_after = today + review_interval_days`. If a human confirmed the
  review, `status: reviewed`; if only you did, leave `draft` and say so.
- **Partially stale** → minimal targeted edits with citations, note the change
  in the commit message; keep/downgrade `confidence`.
- **Conflicting or doubtful** → `status: disputed` + both positions in *Open
  questions* with citations.
- **Superseded** → `status: superseded`, `superseded_by:` pointing to the
  replacement page (create it if needed). Never delete.

## Finish

`python3 scripts/lint.py`, `python3 scripts/dashboard.py`, commit as
`review: <pages> — <outcomes>`. Date bumps and typo fixes are low-risk (commit
directly); claim changes, disputes, and supersedes are medium/high risk — PR
with the reasoning in the description.
