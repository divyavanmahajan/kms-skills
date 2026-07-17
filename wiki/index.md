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
- [LLM interpretability (global workspace)](topics/llm-interpretability.md) —
  Anthropic's J-space research, via The AI Daily Brief

### AI industry (via *The AI Daily Brief*)

Cross-cutting syntheses compiled from 411 AI Daily Brief episode summary notes
(Apr 2025 – mid-2026). All are `draft` / `medium` confidence — third-hand
(podcast coverage of primary reports); see each page's *Open questions*.

- [AI agents (the shift to agentic AI)](topics/ai-agents.md) — adoption curve,
  the "agent boss," swarms, real-world autonomy
- [Vibe coding & AI-assisted software development](topics/vibe-coding.md) —
  Software 3.0, Claude Code, the productivity debate
- [Enterprise AI adoption & strategy](topics/enterprise-ai-adoption.md) —
  use-case frameworks, why pilots fail, ROI
- [Frontier model releases & capabilities](topics/frontier-model-releases.md) —
  the 2025–2026 GPT-5 / Claude / Gemini / Grok timeline
- [AI economics & the bubble debate](topics/ai-economics-and-the-bubble-debate.md) —
  CapEx, valuations, circular financing, the bull/bear case
- [AI, jobs & the labor market](topics/ai-jobs-and-labor.md) — displacement,
  worker sentiment, "AI washing," the counter-narrative
- [AI infrastructure — compute, chips & energy](topics/ai-infrastructure-compute-energy.md) —
  gigawatts, export controls, the grid, token economics
- [AI in media, creativity & society](topics/ai-media-and-society.md) — generative
  media, "AI slop," copyright, the anti-AI turn
- [State of AI — adoption metrics & trends](topics/state-of-ai-adoption.md) — the
  survey/index reports (Stanford, Menlo, a16z, OpenAI/NBER)
- [AI competition, strategy & geopolitics](topics/ai-competition-and-geopolitics.md) —
  the full-stack contest, US–China, AI turning political

## Guides

- [Long-term maintenance guidelines](guides/maintenance-guidelines.md) — every
  concept from the source articles, traced to its implementation here
- [Maintaining the KMS with Obsidian](guides/obsidian.md) — manual editing
  workflow

## Decisions

- [0001 — Repository architecture](decisions/0001-repo-architecture.md)
- [0002 — Adopt a nugget layer](decisions/0002-nugget-layer.md)

## How to add knowledge

Drop material into `inbox/` (or paste a URL) and run `/ingest`. See the
repository `README.md` for the full workflow, and the `policies/` folder for
the rules every page follows.
