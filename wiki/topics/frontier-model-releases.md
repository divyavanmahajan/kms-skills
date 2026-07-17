---
title: Frontier model releases & capabilities (2025–2026)
status: draft
confidence: medium
created: 2026-07-17
review_after: 2026-10-15
review_interval_days: 90
sources:
  - sources/audio/2025-04-08-how-big-a-deal-is-llama-4-s-10m-token-context-window-ad-free.md
  - sources/audio/2025-05-28-what-to-use-claude-4-for.md
  - sources/audio/2025-06-11-what-s-the-bigger-deal-for-ai-o3-pro-or-o3-s-80-price-drop.md
  - sources/audio/2025-07-11-is-grok-4-the-best-llm-yet.md
  - sources/audio/2025-08-07-gpt-5-everything-you-need-to-know.md
  - sources/audio/2025-09-30-claude-sonnet-4-5-can-code-autonomously-for-30-hours.md
  - sources/audio/2025-11-18-how-gemini-3-changes-the-ai-race.md
  - sources/audio/2025-11-26-why-opus-4-5-changes-vibe-coding.md
  - sources/audio/2025-12-11-gpt-5-2-is-here.md
  - sources/audio/2025-12-26-the-5-most-impactful-ai-model-releases-of-2025.md
  - sources/audio/2026-02-06-opus-4-6-and-chatgpt-5-3-codex-are-here-and-the-labs-are-at.md
  - sources/audio/2026-02-20-does-gemini-3-1-pro-matter.md
  - sources/audio/2026-03-06-gpt-5-4-first-test-results.md
  - sources/audio/2026-05-29-claude-opus-4-8-first-impressions.md
tags: [ai-industry, models, benchmarks, ai-daily-brief]
---

# Frontier model releases & capabilities (2025–2026)

## Summary

Over ~15 months the AI Daily Brief chronicles a rapid-fire cadence of frontier
model releases in which leadership rotated among OpenAI (GPT-5 family), Anthropic
(Claude/Opus), and Google (Gemini 3), with xAI's Grok and Meta's Llama as recurring
secondary players. The consistent competitive axis is **coding and agentic
capability** — SWE-Bench, Terminal Bench, ARC-AGI 2, GDP-Val, and OS World recur as
the cited benchmarks — alongside autonomous-session length, token efficiency, and
falling cost-per-task. All benchmark numbers, prices, and version strings are
**third-hand** and frequently reflect the labs' own launch-material claims; several
2026-dated models cannot be independently verified from this corpus — see *Open
questions*.

> This page is a **timeline of reported claims**, not a settled capability ranking.
> The notes themselves repeatedly flag benchmark-gaming, truncated-axis charts, and
> self-selected comparisons.

## The 2025 arc

- **Apr 2025 — Llama 4** (Meta): marketed with a 10M-token context window (Scout)
  and a 17B-active/~400B-total MoE (Maverick), but remembered as a disappointment
  dogged by benchmark-gaming allegations.
- **May 2025 — Claude Opus 4 / Sonnet 4** (Anthropic): a reported ~7-hour coherent
  autonomous refactor set an early "task horizon" marker.
- **Jun 2025 — o3 price drop** (OpenAI): output tokens cut 80% ($40→$8 per million),
  attributed to inference engineering.
- **Jul 2025 — Grok 4** (xAI): a standout 15.9% on ARC-AGI-2 (roughly double the
  prior high) plus a $300/month multi-agent "Heavy" tier.
- **Aug 2025 — GPT-5** (OpenAI): a three-model family (400K context, unified router),
  strong on coding (74.9% SWE-Bench Verified) but widely seen as underwhelming
  versus hype.
- **Sep 2025 — Claude Sonnet 4.5**: a reported 30-hour autonomous coding session
  (~11,000 lines); SWE-Bench cited rising from ~33% to ~82% in a year.
- **Nov 2025 — Gemini 3** (Google): a decisive benchmark leader (31.1% ARC-AGI 2 vs
  GPT-5.1's 17.6%), credited with reversing the "AI plateau" narrative.
- **Nov 2025 — Claude Opus 4.5**: 80.9% SWE-Bench Verified with steep token price
  cuts (see [vibe coding](vibe-coding.md)).
- **Dec 2025 — GPT-5.2** ("Garlic"): 70.9% GDP-Val; ARC Prize cited a ~390x
  one-year cost-efficiency gain on ARC-AGI.

## The 2026 arc

The retrospective ranked Anthropic's Claude suite the #1 release story of 2025, with
reasoning models exceeding 50% of OpenRouter usage by November. Into 2026 the labs
shipped near-simultaneously — Opus 4.6 and GPT-5.3 Codex landed within ~20 minutes
of each other (Feb 2026) — and the frontier moved toward 1M-token context windows,
computer-use (GPT-5.4 reportedly beating a human OS World baseline), and honesty/
anti-sycophancy (Opus 4.8). Gemini 3.1 Pro reportedly jumped ARC-AGI 2 to 77.1% at
under $1/task. By 2026 the notes argue the real battleground had shifted from raw
model capability toward the surrounding "harness" — see
[AI competition & geopolitics](ai-competition-and-geopolitics.md).

## Open questions

- **Third-hand and lab-sourced**: figures are as-reported in episode notes and
  frequently originate from the vendors' own launch materials. Do not treat any
  benchmark, price, or version as confirmed without the primary announcement.
- Several 2026 models and codenames referenced here (GPT-5.4/5.5/5.6, Opus
  4.6/4.7/4.8, Gemini 3.1, "Mythos," "Fable") cannot be verified from this corpus
  and should carry that caveat.
- Benchmarks are not directly comparable across labs (different harnesses, effort
  settings, and test-time compute); the corpus itself flags chart manipulation.

## Sources

- `sources/audio/2025-04-08-how-big-a-deal-is-llama-4-s-10m-token-context-window-ad-free.md` — Llama 4 context window / MoE (`llama4-scout-10m-context`)
- `sources/audio/2025-05-28-what-to-use-claude-4-for.md` — Claude Opus 4 7-hour refactor (`claude-opus4-7hr-refactor`)
- `sources/audio/2025-06-11-what-s-the-bigger-deal-for-ai-o3-pro-or-o3-s-80-price-drop.md` — o3 80% price drop (`o3-price-drop-80pct`)
- `sources/audio/2025-07-11-is-grok-4-the-best-llm-yet.md` — Grok 4 ARC-AGI-2 / Heavy tier (`grok4-arc-agi2-15point9`)
- `sources/audio/2025-08-07-gpt-5-everything-you-need-to-know.md` — GPT-5 family / SWE-Bench (`gpt5-family-400k-context`)
- `sources/audio/2025-09-30-claude-sonnet-4-5-can-code-autonomously-for-30-hours.md` — Sonnet 4.5 30-hour session (`sonnet45-30hr-autonomous`)
- `sources/audio/2025-11-18-how-gemini-3-changes-the-ai-race.md` — Gemini 3 benchmarks (`gemini3-arc-agi2-vs-gpt51`)
- `sources/audio/2025-11-26-why-opus-4-5-changes-vibe-coding.md` — Opus 4.5 SWE-Bench / pricing (`opus-45-swebench-verified-809`, `opus-45-token-price-cut`)
- `sources/audio/2025-12-11-gpt-5-2-is-here.md` — GPT-5.2 GDP-Val, ARC cost-efficiency (`gpt52-gdpval-arcagi`, `arc-390x-cost-efficiency`)
- `sources/audio/2025-12-26-the-5-most-impactful-ai-model-releases-of-2025.md` — 2025 retrospective ranking (`2025-model-retrospective-ranking`)
- `sources/audio/2026-02-06-opus-4-6-and-chatgpt-5-3-codex-are-here-and-the-labs-are-at.md` — near-simultaneous Opus 4.6 / GPT-5.3 (`opus46-gpt53-simultaneous`)
- `sources/audio/2026-02-20-does-gemini-3-1-pro-matter.md` — Gemini 3.1 Pro ARC-AGI 2 (`gemini31-arc-agi2-77`)
- `sources/audio/2026-03-06-gpt-5-4-first-test-results.md` — GPT-5.4 OS World (`gpt54-osworld-above-human`)
- `sources/audio/2026-05-29-claude-opus-4-8-first-impressions.md` — Opus 4.8 benchmarks / honesty (`opus48-benchmarks-honesty`)
