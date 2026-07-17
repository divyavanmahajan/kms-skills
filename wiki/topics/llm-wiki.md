---
title: LLM Wiki (compiled knowledge)
status: draft
confidence: medium
created: 2026-07-17
review_after: 2027-01-13
review_interval_days: 180
sources:
  - sources/web/2026-07-17-what-is-llm-wiki.md
tags: [architecture, knowledge-management]
---

# LLM Wiki (compiled knowledge)

## Summary

An LLM Wiki compiles knowledge at **ingest time** instead of retrieving it at
query time (the RAG approach). Sources are preserved unchanged; an LLM
synthesizes them into structured, cross-linked Markdown pages with provenance,
and a human reviews before pages count as trusted. The result is inspectable,
diffable, portable knowledge — at the cost of ongoing maintenance to prevent
[knowledge drift](knowledge-drift.md).

## Pipeline

1. **Source collection** — originals preserved separately from generated content
2. **Ingestion & extraction** — identify topics, entities, claims, contradictions
3. **Summarization** — compress while preserving argument structure
4. **Structuring** — pages with stable boundaries and recurring formats
5. **Linking** — explicit relationships between concepts
6. **Review** — human verification; non-negotiable where correctness matters

## Design principles

- **Markdown**: "boring formats survive longer than clever platforms"
- **Source separation**: generated pages sit *above* originals, never replace them
- **Provenance**: every page answers "what sources created this?"
- **Fewer, better pages** with meaningful links — over-structuring is a failure mode
- **Mark uncertainty** explicitly (disputed / needs review status)

## Versus RAG

| Dimension | LLM Wiki | RAG |
|-----------|----------|-----|
| Timing | Ingest-time | Query-time |
| Best for | Stable, curated domains | Large, changing corpora |
| Output | Structured pages | Generated answers |

They compose: a hybrid feeds raw sources to both a retrieval layer and the
compiled wiki, with both able to cite the same originals.

## Fit

Good fit: technical documentation, research synthesis, personal knowledge
management, small-team knowledge bases with governance. Poor fit: highly
dynamic data, massive unmanaged corpora, low-quality sources, or any setting
without a review process.

## Division of labor

LLMs summarize, structure, propose links, and detect duplicates. Humans review
accuracy, resolve contradictions, approve publication, and own the system.
See [wiki maintenance](wiki-maintenance.md) for how this repo operationalizes
that split.

## Sources

- `sources/web/2026-07-17-what-is-llm-wiki.md` — supports the whole page
  (summary notes of the glukhov.org article; verbatim quotes preserved there)
