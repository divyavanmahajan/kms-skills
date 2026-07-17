---
url: https://blogs.bing.com/search/June-2026/Announcing-Microsoft-Web-IQ
retrieved: 2026-07-17
type: summary-notes
---

# Announcing Microsoft Web IQ (Bing Search Blog, June 2026) — summary notes

Announced at Microsoft Build 2026 (June 2, 2026). Limited access for selected
developers and enterprises as of retrieval date.

## What it is

"A suite of AI-native grounding APIs built for the agentic era" — a search
engine for AI systems rather than humans. Connects AI systems and agents to
current, real-world intelligence from across the web (web pages, news, images,
videos).

## Architecture layers

1. **Foundation** — the Bing global index: a decades-old corpus maintained for
   freshness, breadth, and trustworthiness.
2. **Model layer** — a small number of world-class models, including a
   best-in-class embedding model projecting information into semantic space.
3. **Retrieval fabric** — distributed infrastructure using DiskANN for
   efficient vector search across disk-resident spaces.
4. **Passage-level output** — returns "passages and structured evidence
   objects" rather than full documents, maximizing information density while
   minimizing token usage.
5. **Orchestration layer** — interprets queries, routes retrieval, merges
   results, adapts to request structure.

## Key claims

- "Models do not need documents, they need information and documents are often
  a poor proxy for that." Passage-level operation concentrates useful signal
  and eliminates irrelevant context — higher information-to-token ratio.
- Quality: higher grounding satisfaction (GDSAT) than competitors.
- Speed: sub-165 ms p95 latency, ~2.5× faster than alternatives (tests across
  five data centers).
- Efficiency: fewer tokens per call via passage-level evidence selection.
- Design philosophy: "fewer tokens in, better answers out, lower cost per
  call." Built for multi-step agentic workflows where retrieval happens
  repeatedly.

## Terminology note

The announcement does NOT use the term "nugget" — the official terms are
"passages" and "structured evidence objects."
