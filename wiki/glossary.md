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
  - sources/web/2026-07-17-webiq-grounding-at-scale.md
  - sources/web/2026-07-17-great-nugget-recall.md
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

The pipeline step that preserves a raw source under `sources/`, extracts
nuggets, and compiles or updates wiki pages from it, with citations. In this
repo: the `/ingest` skill.

## Nugget

A claim-level evidence unit: one atomic claim plus the context that makes it
interpretable on its own (who claims it, when, under what scope) plus
provenance. Also called: *structured evidence object*, *evidence object*
(Microsoft's official Web IQ terms), *passage-level evidence*. Richer than a
chunk. See [Nuggets](topics/nuggets.md); stored under `nuggets/`.

## Nuggetization

Extracting atomic, binary-checkable claims (nuggets) from source material —
originally a manual TREC QA evaluation step (2003), now LLM-automated for RAG
evaluation (AutoNuggetizer, TREC 2024). Also called: *nugget creation*, *fact
extraction*. In this repo, the `/nuggets` skill performs it at ingest time.
See [Nuggets § Heritage](topics/nuggets.md#heritage-nugget-based-evaluation-2003-today).

## Chunk

An arbitrary text window cut from a document for retrieval, typically without
attached context or provenance. What a nugget improves on — see
[Nuggets § versus chunks](topics/nuggets.md#nuggets-versus-chunks).

## Grounding

Supplying an AI system with verifiable, current evidence (rather than relying
on model weights) so its outputs can cite reality. Web IQ is a grounding API;
this repo's wiki pages are grounded via `sources:` frontmatter and nuggets.

<!-- AI industry terms, compiled from The AI Daily Brief corpus (see topics/). -->

## Agent boss

A worker who builds, delegates to, and manages fleets of AI agents rather than
doing all the work directly — Microsoft's framing of the role in the "frontier
firm." See [AI agents](topics/ai-agents.md).

## Agent swarm

A multi-agent architecture where many specialized agents work in parallel,
coordinated by an orchestrator, to converge on an outcome. Also called: *agent
swarms*, *multi-agent systems*. See [AI agents](topics/ai-agents.md).

## Vibe coding

Describing intent in natural language and letting an AI generate working
software; coined by Andrej Karpathy (Feb 2025). Later reframed by some as
*agentic coding* / *spec-driven development*. See [Vibe coding](topics/vibe-coding.md).

## Software 3.0

Andrej Karpathy's framing of LLMs as a third programming paradigm — programmable
in natural language — after human-written code (1.0) and neural-network weights
(2.0). See [Vibe coding](topics/vibe-coding.md).

## Use case primitive

One of OpenAI's six department-agnostic categories of enterprise AI application:
content creation, research, coding, data analysis, ideation & strategy, and
automation. See [Enterprise AI adoption](topics/enterprise-ai-adoption.md).

## Shadow AI

Employees using AI tools (usually personal accounts) without formal
organizational sanction — a gap between individual and organizational adoption.
Also called: *secret cyborgs*. See [Enterprise AI adoption](topics/enterprise-ai-adoption.md).

## AI washing

Citing AI as the reason for layoffs (or product claims) when other factors —
financial pressure, over-hiring — are the real driver, because "AI" reads more
favorably to stakeholders. Also called: *AI laundering*. See
[AI, jobs & labor](topics/ai-jobs-and-labor.md).

## AI slop

Low-quality, mass-produced AI-generated media (text, audio, video, images),
often optimized for algorithmic distribution rather than human value. See
[AI in media, creativity & society](topics/ai-media-and-society.md).

## Circular financing

An arrangement in which a chip/compute vendor invests in an AI lab that then
spends the investment buying the vendor's products, inflating the vendor's
revenue — a central AI-bubble concern. Also called: *vendor financing*. See
[AI economics & the bubble debate](topics/ai-economics-and-the-bubble-debate.md).
