---
title: Nuggets (structured evidence objects)
status: draft
confidence: medium
created: 2026-07-17
review_after: 2026-10-15
review_interval_days: 90
sources:
  - sources/web/2026-07-17-announcing-microsoft-web-iq.md
  - sources/web/2026-07-17-webiq-grounding-at-scale.md
tags: [retrieval, knowledge-management, nuggets]
---

# Nuggets (structured evidence objects)

## Summary

A nugget is a claim-level evidence unit that is richer than a chunk: instead
of an arbitrary text window, it is a passage-level unit "with provenance,
structural metadata, and enough local context to remain interpretable when
detached from the source page." The optimization target shifts from *document
relevance* to *information density per token*. Microsoft's Web IQ (announced
at Build 2026) is the highest-profile production example; its official terms
are "passages" and "structured evidence objects" — *nugget* is the community
shorthand. This repo adopts the idea as a claim inventory between sources and
compiled pages (see [how this repo uses nuggets](#how-this-repo-uses-nuggets)).

## Nuggets versus chunks

| | Chunk | Nugget / evidence object |
|---|---|---|
| Unit | Fixed or heuristic text window | One self-contained claim/passage |
| Selected by | Document relevance | Information density per token, relative to the query |
| Context | Whatever fell inside the window | Explicitly attached (who/when/scope, resolved references) |
| Provenance | Often lost after splitting | Carried on the unit; outputs stay inspectable |
| Detached use | Frequently uninterpretable alone | Designed to stand alone off-page |

The economic argument: better evidence units reduce prompt size, concentrate
the relevant facts for reasoning, and preserve attribution — "fewer tokens in,
better answers out, lower cost per call."

## How Web IQ produces them

In Web IQ's stack (Bing index → embedding models → DiskANN-based retrieval
fabric → orchestration), evidence objects are created in the orchestration
layer's **context-construction phase**: dense retrieval yields candidate
passages from the semantic index, then a selection component packages the
densest evidence under latency and context-window constraints. Microsoft
reports sub-165 ms p95 latency and frames the whole design as token-economics
optimization rather than architectural novelty.

## How this repo uses nuggets

This knowledge base compiles at ingest time, so nugget extraction happens
during `/ingest` rather than at query time: each source gets a
`nuggets/<slug>.yaml` claim inventory per `policies/nugget-policy.md`. The `context`
field carries what Web IQ calls local context (who claims it, when, under what
scope), and provenance is the `source` path. Downstream, nuggets make
[maintenance](wiki-maintenance.md) mechanical: contradiction sweeps compare
claims instead of prose, and citation-drift checks verify pages against the
inventory. See the [LLM wiki](llm-wiki.md) page for where this sits in the
architecture.

## Open questions

- "Nugget" as an evaluation unit predates Web IQ (TREC QA's nugget-based
  evaluation and recent RAG-evaluation "nuggetization" work) — no source for
  this is ingested yet, so it is recorded here as unsourced background.
- All Web IQ performance figures (GDSAT, latency, token efficiency) are
  vendor-reported; no independent benchmarks ingested yet.

## Sources

- `sources/web/2026-07-17-announcing-microsoft-web-iq.md` — product framing,
  architecture layers, performance claims (nuggets: `webiq-passage-output`,
  `webiq-p95-latency`, `webiq-architecture-layers`)
- `sources/web/2026-07-17-webiq-grounding-at-scale.md` — evidence-object
  definition, contrast with chunks, pipeline position (nuggets:
  `evidence-object-definition`, `evidence-object-vs-chunk`,
  `evidence-object-pipeline-position`)
