---
title: "0002: Adopt a nugget layer between sources and wiki"
status: reviewed
confidence: high
created: 2026-07-17
reviewed: 2026-07-17
review_after: 2031-07-16
sources:
  - sources/web/2026-07-17-webiq-grounding-at-scale.md
tags: [decision, nuggets]
---

# 0002: Adopt a nugget layer between sources and wiki

## Context

Sources are prose; wiki pages are synthesis. Between them there was no
machine-checkable claim inventory, so contradiction sweeps and citation-drift
checks required an LLM to re-read prose every time. Microsoft Web IQ's
[structured evidence objects](../topics/nuggets.md) demonstrate a better unit:
claim-level, context-enriched, provenance-carrying.

## Decision

Add `nuggets/` — one YAML file per source, each nugget an atomic claim with
`context` (who/when/scope, resolved references), optional verbatim `quote`,
`confidence`, and `status`, governed by `policies/nugget-policy.md`. Extraction is
part of `/ingest` (and available standalone as `/nuggets`). Claims are
immutable once recorded — corrections supersede, never rewrite. `lint.py`
validates the schema and id uniqueness; the dashboard counts the inventory.

## Consequences

- Contradiction sweeps start from structured claims instead of re-reading
  prose — cheaper and more repeatable.
- Citation checks can verify a page against specific nugget ids.
- Ingestion costs more effort per source (extraction is judgment work).
- The inventory itself can drift; nugget files inherit the same
  supersede-don't-delete discipline as wiki pages.
