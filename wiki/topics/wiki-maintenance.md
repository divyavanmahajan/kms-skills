---
title: Wiki maintenance
status: draft
confidence: medium
created: 2026-07-17
review_after: 2027-01-13
review_interval_days: 180
sources:
  - sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md
tags: [maintenance, operations]
---

# Wiki maintenance

## Summary

Maintenance keeps the wiki "useful, inspectable, and recoverable" — not
perfect. The system must always be able to answer two questions: *what sources
support this claim?* and *can we roll back a bad update?* Git provides the
rollback; policies, lint, and scheduled reviews provide the rest. This page
describes the operating model this repository implements against
[knowledge drift](knowledge-drift.md).

## The maintenance loop

source addition → compilation → link updates → structural lint → semantic
review → human approval → committed changes → scheduled staleness reviews.

In this repo: `/ingest` covers the first three, `scripts/lint.py` the fourth,
`/review` and `/contradictions` the fifth, risk-tiered PRs the sixth, and the
weekly GitHub Action drives the cycle.

## Operating files

Four files define agent behavior — all present in this repo:

- `AGENTS.md` — what agents may change and how (small diffs, risk tiers)
- `policies/schema.md` — page structure, so updates are predictable
- `policies/citation-policy.md` — what requires sources
- `policies/source-policy.md` — originals preserved, dated, never discarded

## Automation split

- **Structural lint** (fully automatable): broken links, orphans, missing
  metadata, naming. Validates *maintainability, not truth*.
- **Semantic checks** (LLM-assisted, human-approved): unsourced claims,
  incompatible pages, outdated decisions — flagged, never auto-rewritten.
- **Contradiction detection**: extract claims → find related pages → classify
  (actual contradiction vs. version/scope difference) → resolve by
  superseding, splitting contexts, or preserving the disagreement explicitly.

## Risk tiers and cadences

Changes are partitioned into low / medium / high risk (see
`policies/review-policy.md`), with review intervals per content type: pricing
7–30 days, tool pages 30–90 days, principles 6–18 months, historical records
only when superseded. Structural lint runs on every push and weekly; staleness
review weekly; citation checks before any draft is promoted.

## Health metrics

Tracked on the [dashboard](../dashboard.md): pages by status, sourced vs.
unsourced, pages past review date, broken links, orphans, low-confidence
pages, stale percentage.

For the full operating rules with concept-to-implementation traceability, see
the [long-term maintenance guidelines](../guides/maintenance-guidelines.md).

## Sources

- `sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md` — supports
  the loop, operating files, risk tiers, cadences, and metrics
