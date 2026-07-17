---
title: Knowledge drift
status: draft
confidence: medium
created: 2026-07-17
review_after: 2027-01-13
review_interval_days: 180
sources:
  - sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md
tags: [maintenance, knowledge-management]
---

# Knowledge drift

## Summary

Knowledge drift is compiled content becoming disconnected from reality. It is
the central failure mode of an [LLM wiki](llm-wiki.md): unlike raw sources, "a
summary you already compiled has to be actively kept honest." Six distinct
mechanisms cause it, and each needs a different countermeasure — see
[wiki maintenance](wiki-maintenance.md).

## The six mechanisms

| Drift | What happens | Primary countermeasure |
|---|---|---|
| **Source drift** | Underlying materials change (versions, APIs, policies); old claims become outdated | Review intervals per content type; re-ingest sources |
| **Concept drift** | Terms shift meaning over time; pages silently merge incompatible ideas | Glossary with dated definitions; split pages by meaning |
| **Terminology drift** | Multiple names for one concept break search and linking | Record aliases in the glossary; normalize links |
| **Decision drift** | Superseded decisions stay documented as current practice | Decision records with proposed/accepted/superseded status |
| **Citation drift** | After rewrites, claims no longer match cited sources — "false confidence" | Citation check before publishing; re-verify claims on review |
| **Structure drift** | New pages proliferate instead of updates; orphans and duplicates accumulate | Structural lint (orphans, broken links); prefer updates over new pages |

## Why it matters

Citation drift is the most insidious: a page that *looks* sourced but isn't is
worse than an openly unsourced one. Structure drift is the most visible:
navigability decays until nobody trusts the wiki enough to read it.

## Sources

- `sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md` — supports
  the six mechanisms and the quoted maintenance principle
