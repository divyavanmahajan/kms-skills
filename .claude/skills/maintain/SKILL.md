---
name: maintain
description: Run the full weekly maintenance loop — ingest anything in inbox/, structural lint, staleness review, contradiction spot-check, dashboard regeneration — and open a PR with the changes. Used by the scheduled GitHub Action and on demand ("run maintenance").
---

# Weekly maintenance loop

Follow `AGENTS.md`. This orchestrates the other skills; keep the total diff
small enough for a human to review in minutes.

## Loop

1. **Inbox** — if `inbox/` has files, run the `ingest` skill's procedure on them.
2. **Structural lint** — `python3 scripts/lint.py`. Fix all errors and the cheap
   warnings (broken links, missing metadata, orphans → add a link from the
   relevant topic page or index). These fixes are low-risk.
3. **Staleness** — `python3 scripts/dashboard.py`, then run the `review` skill's
   procedure on the 3 most overdue pages (skip if none are stale).
4. **Contradiction spot-check** — only if step 1 ingested something or step 3
   changed claims: check the touched concepts against related pages (the
   `contradictions` skill's classification applies).
5. **Graph entity coverage** — `python3 scripts/extract_entities.py --check`.
   For any nugget it lists, read that nugget and add its entities to
   `graph/entities.yaml` (rules: `SYSTEM_PROMPT` in
   `scripts/extract_entities.py`; reuse existing entity names — see the
   `ingest` skill's Step 3b). Additive cache entries are low-risk. If the
   `kms_mcp` dependencies are installed, finish with `python3 -m kms_mcp index`
   so the local knowledge graph reflects the session (`.kms-index/` is
   gitignored — nothing to commit).
6. **Regenerate** — `python3 scripts/dashboard.py` again so the dashboard
   reflects the session's fixes.

## Committing (CI context)

- If everything is low-risk (link/metadata fixes + dashboard): commit directly
  to the current branch as `lint: weekly maintenance` + `dashboard: regenerate`.
- If anything is medium/high-risk (claim edits, disputes, supersedes, new
  pages): create a branch `maintenance/YYYY-MM-DD`, commit there, push, and
  open a PR titled `Weekly maintenance YYYY-MM-DD` whose description lists each
  change with its risk tier and what needs human eyes. Never merge it yourself.
- If there is nothing to do, say so and stop — do not create empty commits.

## Report

End with a short summary: pages reviewed, fixes applied, disputes raised, PR
link if one was opened, and the headline dashboard numbers.
