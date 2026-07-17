---
url: https://www.glukhov.org/knowledge-management/knowledge-systems-architectures/compiled-knowledge/what-is-llm-wiki/
retrieved: 2026-07-17
type: summary-notes
---

# What is an LLM Wiki (glukhov.org) — summary notes

## Core concept

An LLM Wiki performs synthesis at **ingestion time** rather than query time:
"RAG retrieves knowledge at query time. LLM Wiki compiles knowledge at ingest
time." This timing difference shapes cost, latency, quality, and maintenance.

Instead of storing raw documents for retrieval, it creates structured
wiki-like knowledge: topic pages, summaries, glossaries, comparisons,
cross-links. Output is human-readable Markdown — "inspectable, portable,
editable, versionable, easy to diff, compatible with static sites and PKM
tools."

## Building pipeline

1. Source collection — preserve originals separately from generated content
2. Ingestion & extraction — identify topics, entities, claims, contradictions
3. Summarization — compress while preserving argument structure
4. Structuring — pages with stable boundaries and recurring formats
5. Linking — explicit relationships between concepts
6. Review — human verification (non-negotiable for reliability)

## Design principles

- Markdown format: "Boring formats survive longer than clever platforms"
- Source separation: never replace originals; generated pages sit above them
- Provenance: every page answers "What sources created this?"
- Quality over quantity: "Prefer fewer better pages" with meaningful links
- Uncertainty marking: status indicators like "disputed" or "needs review"

## LLM Wiki vs RAG

| Dimension | LLM Wiki | RAG |
|-----------|----------|-----|
| Timing | Ingest-time | Query-time |
| Best for | Stable, curated domains | Large, changing corpora |
| Output | Structured pages | Generated answers |

Complementary, not competing: RAG gives flexible access; LLM Wiki gives
reusable synthesis. Hybrid: raw sources feed both a RAG layer and the wiki.

## Good and bad fits

Good: technical documentation/concepts, research synthesis, personal knowledge
management, technical blogging, small-team knowledge bases with governance.
Bad: highly dynamic data, massive unmanaged corpora, low-quality sources,
no review process.

## Limitations

- Maintenance drift — generated pages go stale as sources change
- Hallucinated synthesis — wrong summaries embedded as authority
- Over-structuring — too many pages of unclear value
- Ownership ambiguity — without clear responsibility, systems decay

## Roles

LLMs: summarize, structure, propose links, detect duplicates.
Humans: review accuracy, resolve contradictions, approve publication, own the
system, decide what deserves representation. "Generated structure needs
provenance, and every important claim should link back to its original
sources."
