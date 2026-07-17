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
  - sources/web/2026-07-17-great-nugget-recall.md
  - sources/web/2026-07-17-autonuggetizer-trec-2024-rag.md
  - sources/web/2026-07-17-trec-2007-qa-overview.md
tags: [retrieval, knowledge-management, nuggets, evaluation]
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

## Heritage: nugget-based evaluation (2003 → today)

The term has a two-decade evaluation lineage predating Web IQ. Voorhees
introduced nugget-based evaluation in the **2003 TREC Question Answering
Track** for definition questions that required synthesizing multiple
documents: a nugget there is "a discrete factual assertion for which
assessors can make binary determinations about presence in responses,"
judged semantically, with facts classified **vital** (must appear in a good
answer) or **okay** (helpful, not essential). **Nugget pyramids** (TREC
2006–2007) refined this by pooling importance judgments from multiple
assessors; pre-LLM automation attempts (POURPRE, Nuggeteer, 2005–2006)
stalled on the technology of the time.

The modern revival is **nuggetization** for RAG evaluation: the
**AutoNuggetizer** framework (TREC 2024 RAG Track, Pradeep et al.) uses LLMs
to both create nuggets from relevant documents and assign them
(support / partial / no support) against system answers. Fully automatic
evaluation ranks systems almost as reliably as human assessors (run-level
Kendall's τ 0.783 in the track report, 0.887–0.901 in the follow-up study),
though per-answer agreement is noisier, LLM judges are stricter than humans,
and hybrid pipelines (human-edited nuggets + automatic assignment) agree best.

The evaluation lineage and Web IQ's retrieval units converge on the same
insight this repo builds on: **the atomic, attributable claim — not the
document or the chunk — is the right unit for judging and carrying
knowledge.** Our `nuggets/` inventory is simultaneously a Web-IQ-style
evidence store and a TREC-style claim checklist a review can score pages
against.

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

- All Web IQ performance figures (GDSAT, latency, token efficiency) are
  vendor-reported; no independent benchmarks ingested yet.
- The TREC 2007 overview source is a thin snapshot (search excerpts only) —
  expand it from the full PDF before promoting pyramid-related claims.

*(Resolved 2026-07-17: the TREC heritage of "nugget" was previously recorded
here as unsourced background; now sourced — see Heritage section.)*

## Sources

- `sources/web/2026-07-17-announcing-microsoft-web-iq.md` — product framing,
  architecture layers, performance claims (nuggets: `webiq-passage-output`,
  `webiq-p95-latency`, `webiq-architecture-layers`)
- `sources/web/2026-07-17-webiq-grounding-at-scale.md` — evidence-object
  definition, contrast with chunks, pipeline position (nuggets:
  `evidence-object-definition`, `evidence-object-vs-chunk`,
  `evidence-object-pipeline-position`)
- `sources/web/2026-07-17-great-nugget-recall.md` — 2003 origin, evaluation
  definition, POURPRE/Nuggeteer, automation correlations (nuggets:
  `nugget-eval-definition`, `nugget-eval-origin-2003`, `pre-llm-automation`,
  `nuggetization-correlation`)
- `sources/web/2026-07-17-autonuggetizer-trec-2024-rag.md` — AutoNuggetizer
  pipeline, vital/okay scoring, TREC 2024 correlations (nuggets:
  `autonuggetizer-what`, `autonuggetizer-pipeline`, `vital-vs-okay`,
  `autonuggetizer-correlation`)
- `sources/web/2026-07-17-trec-2007-qa-overview.md` — nugget pyramids
  (nugget: `nugget-pyramid`; thin snapshot)
