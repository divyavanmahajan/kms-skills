---
title: AI agents (the shift to agentic AI)
status: draft
confidence: medium
created: 2026-07-17
review_after: 2026-10-15
review_interval_days: 90
sources:
  - sources/audio/2025-04-21-agent-pilots-nearly-doubled-last-quarter.md
  - sources/audio/2025-04-25-how-every-employee-becomes-an-agent-boss.md
  - sources/audio/2025-07-29-walmart-blasts-past-agent-experimentation.md
  - sources/audio/2025-09-19-ai-agent-deployments-quadruple-in-2025.md
  - sources/audio/2025-10-12-what-1-000-execs-told-us-about-ai-agents.md
  - sources/audio/2025-10-26-workers-are-excited-about-ai-agents-so-why-are-companies-scr.md
  - sources/audio/2025-11-09-a-framework-for-choosing-winning-ai-use-cases-agent-readines.md
  - sources/audio/2026-01-26-ralph-wiggum-clawdbot-and-mac-minis-how-pros-are-vibe-coding.md
  - sources/audio/2026-01-28-are-agent-swarms-the-next-ai-paradigm.md
  - sources/audio/2026-02-05-the-dawn-of-the-agent-age.md
  - sources/audio/2026-02-19-how-people-actually-use-ai-agents.md
  - sources/audio/2026-05-24-why-agents-still-need-humans.md
tags: [ai-industry, agents, enterprise, ai-daily-brief]
---

# AI agents (the shift to agentic AI)

## Summary

Across 2025–2026, *The AI Daily Brief* frames the central story of enterprise AI
as a shift from AI-as-assistant to AI-as-agent: software that plans and executes
multi-step tasks with tools, not just answers prompts. Quarterly KPMG surveys
tracked enterprise agent deployment rising from ~11% to ~42% of large firms
across 2025, while the endpoint is framed as the Microsoft "frontier firm" where
every employee becomes an "[agent boss](../glossary.md#agent-boss)." A recurring
finding is that the binding constraints are organizational (data fragmentation,
governance, change management) rather than technical, and that by 2026 the frontier
had moved to multi-agent [swarms](../glossary.md#agent-swarm) and to measuring
real-world autonomy — where median agent turns are short even as the capability
ceiling grows. All claims here are **third-hand**: owner's summary notes of a
podcast that itself synthesizes primary studies — see *Open questions*.

## Adoption moved from pilots to deployment

The quarter-by-quarter data (as relayed from KPMG's AI Quarterly Pulse Survey of
~130 firms with $1B+ revenue) traces a fast climb: agent *piloting* jumped from
37% to 65% in Q1 2025 while full deployments held at 11%; by Q3 2025 *deployment*
had reached 42% — nearly a fourfold rise across the year — and reported employee
resistance fell from 47% to 21%. Consumer-and-worker sentiment tracked the same
way: an EY study put 84% of employees "eager" to use agentic AI, though a majority
worried about job security.

## The "frontier firm" and the agent boss

Microsoft/LinkedIn's 2025 Work Trend Index supplies the dominant organizing
metaphor: the "frontier firm" evolves through three phases — human with assistant,
human-agent teams, and human-led/agent-operated — and reframes managers as "agent
bosses" who build, delegate to, and supervise fleets of agents. Walmart is the
recurring enterprise case study, organizing a company-wide framework around four
orchestration-layer "super agents" (for customers, suppliers, employees, and
developers).

## Barriers are organizational, not technical

Super Intelligent's audits of 1,000+ organizations produced an Agent Readiness
Score averaging 52.1/100 (most firms in the "Agent Pilot" tier), with an AI
governance framework worth ~6.6 points on average. The single biggest blocker was
**data fragmentation**, not legacy technology; undocumented processes and weak
change management recur across the corpus. Communication mattered measurably:
agentic-AI usage was 66% at firms that clearly communicate their AI strategy
versus 39% at those that do not. See [enterprise AI adoption](enterprise-ai-adoption.md)
for the frameworks (use-case primitives, agent-readiness, maturity maps) that grew
up around this problem.

## From single agents to swarms — and back to humans

By 2026 the notes pivot to multi-agent parallelization: Moonshot's Kimi K2.5 trains
"agent swarms" via PARL (Parallel Agent Reinforcement Learning) to combat "serial
collapse," and practitioners run planner/worker/judge loops at scale (see
[vibe coding](vibe-coding.md)). Yet Anthropic's autonomy study found the *median*
Claude Code turn lasts ~45 seconds even as the 99.9th-percentile turn grew toward
~45 minutes — a "capability overhang" between what agents can do and how they are
actually used — and that more than half of agentic tool calls already fall outside
coding. The 2026 episodes reframe the human role: rather than eliminating work,
agents create an "infinite backlog" in a "human sandwich" (human frames, AI
collapses the task, human judges and extends), a thread continued in
[AI, jobs & labor](ai-jobs-and-labor.md).

## Why it matters for this knowledge base

This is the most sustained theme in the AI Daily Brief corpus and the connective
tissue between the other pages here — [enterprise adoption](enterprise-ai-adoption.md),
[vibe coding](vibe-coding.md), and [jobs](ai-jobs-and-labor.md) are all, in part,
agent stories. The 90-day review interval reflects how fast the framing moves.

## Open questions

- Everything here is **third-hand** — owner's summary notes of AI Daily Brief
  episodes that themselves relay primary studies (KPMG, Microsoft/LinkedIn, EY,
  Anthropic, Moonshot). Verify against the primary reports before promoting any
  figure past `draft`/`medium`.
- Survey figures come from vendors and consultancies with an interest in the
  narrative (KPMG, Super Intelligent, EY); adoption definitions vary across
  surveys, so the quarter-over-quarter series may not be strictly comparable.
- The "capability overhang" and swarm claims are recent and largely unreplicated.

## Sources

- `sources/audio/2025-04-21-agent-pilots-nearly-doubled-last-quarter.md` — KPMG Q1 2025 pilot/deployment figures (nugget: `kpmg-agent-pilots-2025`)
- `sources/audio/2025-09-19-ai-agent-deployments-quadruple-in-2025.md` — KPMG Q3 2025 deployment + resistance (`kpmg-agent-deployment-quadruple-2025`, `kpmg-worker-resistance-collapse-q3-2025`)
- `sources/audio/2025-04-25-how-every-employee-becomes-an-agent-boss.md` — Microsoft frontier firm / agent boss (`msft-agent-boss-82pct-capacity`, `frontier-firm-three-phases`)
- `sources/audio/2025-10-12-what-1-000-execs-told-us-about-ai-agents.md` — Agent Readiness Score, data fragmentation (`agent-readiness-score-52`, `data-fragmentation-top-blocker`)
- `sources/audio/2025-10-26-workers-are-excited-about-ai-agents-so-why-are-companies-scr.md` — EY worker sentiment + communication gap (`ey-84pct-eager-agents`, `clear-communication-agent-usage-gap`)
- `sources/audio/2025-07-29-walmart-blasts-past-agent-experimentation.md` — Walmart four super agents (`walmart-four-super-agents`)
- `sources/audio/2026-01-28-are-agent-swarms-the-next-ai-paradigm.md` — Kimi K2.5 / PARL swarms (`kimi-k25-parl-swarm`)
- `sources/audio/2026-02-19-how-people-actually-use-ai-agents.md` — Anthropic autonomy study (`claude-code-median-turn-45s`, `agentic-use-beyond-coding`)
- `sources/audio/2026-02-05-the-dawn-of-the-agent-age.md` — "dawn of the agent age" (`dawn-agent-age-jan-2026`)
- `sources/audio/2026-05-24-why-agents-still-need-humans.md` — infinite backlog / human sandwich (`human-sandwich-infinite-backlog`)
- `sources/audio/2026-01-26-ralph-wiggum-clawdbot-and-mac-minis-how-pros-are-vibe-coding.md` — parallel-agent orchestration (`cursor-browser-parallel-agents`)
- `sources/audio/2025-11-09-a-framework-for-choosing-winning-ai-use-cases-agent-readines.md` — agent-readiness use-case framework (`gaspar-four-step-use-case-process`, `kpmg-ceo-roi-timeline`)
