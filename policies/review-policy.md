# review-policy.md — Risk Tiers and Review Cadences

Goal: keep the wiki **useful, inspectable, and recoverable** — not perfect.
Review effort is partitioned by risk and by how fast content type decays.

## Risk tiers

| Tier | Change types | Process |
|------|--------------|---------|
| **Low** | Link fixes, typos, formatting, aliases, tag updates, dashboard regeneration | Agent commits directly; Git diff is the review |
| **Medium** | New topic pages, new summaries, updated recommendations, glossary changes | PR; human skims and merges |
| **High** | Deleting/superseding claims, changes to canonical pages, security/pricing/version claims, edits to `policies/` or `AGENTS.md` | PR with explicit human approval; agents never merge |

## Review intervals by content type

Set `review_interval_days` in page frontmatter accordingly:

| Content type | Interval |
|---|---|
| Pricing / limits / quotas | 7–30 days |
| Tool & product pages | 30–90 days |
| Technique / how-to pages | 90–180 days |
| Architecture principles, concepts | 180–540 days |
| Decision records, historical pages | No interval — review only when superseded |

## Cadences

- **Structural lint** — every push (CI) and weekly scheduled run
- **Staleness review** — weekly: dashboard flags pages past `review_after`; the
  scheduled maintenance session reviews the oldest ones and opens a PR
- **Citation check** — before every `draft → reviewed` transition
- **Contradiction sweep** — monthly, or after any large ingest

## What a semantic review checks

1. Do the claims still match the cited sources? (citation drift)
2. Have the underlying facts changed? (source drift — may require re-ingesting)
3. Does the terminology still match the glossary? (terminology drift)
4. Is a recorded decision still current practice? (decision drift)
5. Outcome: bump `reviewed`/`review_after`, or mark `disputed`/`superseded`
   with reasons in *Open questions*.

## Health metrics (tracked in `wiki/dashboard.md`)

Page count by status, sourced vs. unsourced pages, pages past review date,
broken links, orphan pages, low-confidence pages, stale percentage.
