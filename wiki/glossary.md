---
title: Glossary
status: draft
confidence: medium
created: 2026-07-17
review_after: 2027-01-13
review_interval_days: 180
sources:
  - sources/web/2026-07-17-what-is-llm-wiki.md
  - sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md
tags: [glossary]
---

# Glossary

Canonical terms for this knowledge base. Aliases are recorded explicitly to
fight terminology drift — if you meet a synonym in the wild, add it here
rather than renaming pages.

## LLM Wiki

A knowledge system that compiles sources into structured, cross-linked
Markdown pages at ingest time. Also called: *compiled knowledge base*,
*compiled knowledge architecture*. See [LLM Wiki](topics/llm-wiki.md).

## RAG (Retrieval-Augmented Generation)

Query-time retrieval of raw document chunks fed to an LLM to generate answers.
The complementary architecture to an LLM wiki. See
[LLM Wiki § Versus RAG](topics/llm-wiki.md#versus-rag).

## Knowledge drift

Compiled content becoming disconnected from reality. Six mechanisms: source,
concept, terminology, decision, citation, and structure drift. See
[Knowledge drift](topics/knowledge-drift.md).

## Provenance

The traceable link from a compiled claim back to the raw source that supports
it. Recorded in page frontmatter (`sources:`) and each page's *Sources*
section.

## Supersede

The only sanctioned way to retire content: mark the page
`status: superseded`, point `superseded_by` at the replacement, keep the file.
Nothing is deleted.

## Staleness

A page past its `review_after` date. Stale ≠ wrong — it means the page's
claims haven't been re-verified within the interval its content type requires.

## Ingest

The pipeline step that preserves a raw source under `sources/` and compiles or
updates wiki pages from it, with citations. In this repo: the `/ingest` skill.
