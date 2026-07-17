---
title: Knowledge Base
status: reviewed
confidence: high
created: 2026-07-17
reviewed: 2026-07-17
review_after: 2027-07-17
review_interval_days: 365
sources: []
tags: [navigation]
---

# Knowledge Base

This is a **compiled knowledge system** (an "LLM wiki"): raw sources are
preserved under `sources/`, and the pages here are synthesized from them —
with provenance — by LLM-assisted ingestion, then kept honest by scheduled
maintenance.

## Start here

- [Health Dashboard](dashboard.md) — what needs attention right now
- [Glossary](glossary.md) — canonical terms and aliases

## Topics

- [LLM Wiki (compiled knowledge)](topics/llm-wiki.md) — the architecture this
  repo implements
- [Knowledge drift](topics/knowledge-drift.md) — the six ways compiled
  knowledge rots
- [Wiki maintenance](topics/wiki-maintenance.md) — how this repo fights drift
- [Nuggets (structured evidence objects)](topics/nuggets.md) — claim-level
  evidence units, richer than chunks

## Decisions

- [0001 — Repository architecture](decisions/0001-repo-architecture.md)
- [0002 — Adopt a nugget layer](decisions/0002-nugget-layer.md)

## How to add knowledge

Drop material into `inbox/` (or paste a URL) and run `/ingest`. See the
repository `README.md` for the full workflow, and the `policies/` folder for
the rules every page follows.
