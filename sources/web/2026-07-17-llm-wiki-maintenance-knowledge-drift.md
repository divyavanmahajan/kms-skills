---
url: https://www.glukhov.org/knowledge-management/knowledge-systems-architectures/compiled-knowledge/llm-wiki-maintenance-knowledge-drift/
retrieved: 2026-07-17
type: summary-notes
---

# LLM Wiki maintenance & knowledge drift (glukhov.org) — summary notes

## Six drift mechanisms

1. **Source drift** — underlying materials change (tool versions, APIs,
   policies); old claims become outdated despite historical accuracy.
2. **Concept drift** — terms like "agent" or "RAG" shift meaning; pages
   silently merge incompatible ideas.
3. **Terminology drift** — multiple names for one concept break search and
   linking.
4. **Decision drift** — superseded decisions stay documented as current
   practice.
5. **Citation drift** — after rewrites, claims no longer match their cited
   sources ("false confidence").
6. **Structure drift** — new pages proliferate instead of updating existing
   ones; orphans and duplicates accumulate.

## Core strategy

Goal: keep the wiki "useful, inspectable, and recoverable" — not perfect.
Key questions: "What sources support this claim?" and "Can we roll back a bad
update?"

Repeatable loop: source addition → compilation → link updates → structural
linting → semantic review → human approval → committed changes → scheduled
staleness reviews.

## Operating files

1. **AGENTS.md** — rules for what agents may modify (small updates over
   rewrites; review for risky changes)
2. **schema.md** — consistent page structure for predictable updates
3. **citation-policy.md** — what requires sources (technical claims,
   comparisons, version-specific statements, benchmarks)
4. **source-policy.md** — preserve originals, record dates, never discard

"A summary you already compiled has to be actively kept honest."

## Automation

- **Structural linting** (automatable): broken links, orphans, missing
  metadata, inconsistent naming. Validates maintainability, not truth.
- **Semantic checking** (harder): unsourced claims, incompatible pages,
  outdated decisions, version-specific statements — flag, don't auto-rewrite.
- **Contradiction detection**: extract claims → find related pages → classify
  conflict type (actual contradiction vs. version/scope difference).
  Resolutions: mark superseded, split contexts, preserve disagreement, update
  decision records.

## Risk tiers and cadences

- Low risk: link fixes, formatting, aliases — minimal review
- Medium: new summaries, concept pages, recommendations — standard review
- High: claim deletions, canonical page changes, security/pricing — human
  approval required

Review intervals: tool pages 30–90 days; pricing 7–30 days; architecture
principles 6–18 months; historical records only when superseded.

Cadence: structural lint weekly, stale reviews monthly, citation checks before
publishing.

## Metrics and practices

Health metrics: page count, sourced vs. unsourced, pages past review dates,
broken links, orphan pages, contradiction reports, stale percentage.

Practices: Git diffs to review agent changes; commit messages that explain
operations ("ingest: add source notes"); Markdown dashboards for stale
pages/contradictions/broken links; metadata blocks with review dates and
confidence; archive or supersede rather than delete; link superseded pages to
replacements; split canonical pages from version-specific content; avoid agent
rewrites larger than necessary.

Success criterion: "inspectable knowledge that can be reviewed, repaired, and
trusted over time" — transparency over perfection.
