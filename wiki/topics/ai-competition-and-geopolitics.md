---
title: AI competition, strategy & geopolitics
status: draft
confidence: medium
created: 2026-07-17
review_after: 2026-10-15
review_interval_days: 90
sources:
  - sources/audio/2025-05-03-nvidia-and-anthropic-trade-barbs-around-ai-chip-rules.md
  - sources/audio/2025-05-31-nvidia-ceo-says-china-ai-is-catching-up-fast.md
  - sources/audio/2025-12-10-the-ai-race-gets-a-massive-power-shift.md
  - sources/audio/2025-12-10-the-state-of-enterprise-ai.md
  - sources/audio/2026-01-03-what-manus-and-groq-acquisitions-tell-us-about-ai.md
  - sources/audio/2026-02-11-how-the-global-ai-race-has-shifted.md
  - sources/audio/2026-02-28-who-controls-ai.md
  - sources/audio/2026-03-06-ai-is-officially-political.md
  - sources/audio/2026-04-16-ai-s-great-divergence.md
  - sources/audio/2026-04-27-how-deepseek-v4-connects-to-the-us-power-grid.md
  - sources/audio/2026-04-29-ai-lab-power-rankings.md
  - sources/audio/2026-05-07-surprise-elon-anthropic-team-up-reshapes-the-ai-race.md
  - sources/audio/2026-06-02-should-americans-get-shares-in-ai-companies.md
  - sources/audio/2026-06-27-the-ad-hoc-ai-licensing-regime-ai-weekly-brief.md
  - sources/audio/2026-02-06-opus-4-6-and-chatgpt-5-3-codex-are-here-and-the-labs-are-at.md
tags: [ai-industry, competition, strategy, geopolitics, ai-daily-brief]
---

# AI competition, strategy & geopolitics

## Summary

The AI Daily Brief traces a decisive shift in how AI competition is framed: away
from raw model benchmarks and toward a full-stack contest over compute ownership,
energy, inference hardware, distribution/app-layer control, and geopolitical
positioning. A recurring argument holds that the binding constraint is compute and
token supply rather than share of a fixed pie — so multiple labs can win at once,
while cloud/infrastructure providers structurally capture value. The US–China axis
dominates the geopolitical thread, and by 2026 AI had become an overt political
issue at home (the Anthropic–Pentagon standoff, an "ad hoc licensing regime"). All
figures are **third-hand** — one host's analysis as captured in episode notes — see
*Open questions*.

## The competitive axis moved down the stack

The notes repeatedly reframe competition around compute/infrastructure, energy, and
the agent "harness" layer (Claude Code vs. Codex) rather than benchmarks alone (see
[frontier model releases](frontier-model-releases.md)). A consolidation/acqui-hire
wave — Meta–Manus (>$2B), NVIDIA–Groq ($20B licensing) — is read as bets on the
agentic app layer and the inference bottleneck. Anthropic's share of enterprise LLM
spend overtaking OpenAI's (see [state of AI](state-of-ai-adoption.md)) and a PwC
finding that ~75% of AI's gains accrue to the top 20% of firms ("AI's great
divergence") reinforce a winner-take-more dynamic — even as the "zero-sum" framing
is rejected because token demand is growing faster than infrastructure can serve it.

## Deals and lab positioning

Structural deals recur: an amended Microsoft–OpenAI partnership (ending cloud
exclusivity, a 27% stake and ~20% revenue share through 2030, dropping the "AGI
clause"); Google's $40B into Anthropic; and Anthropic leasing xAI's Colossus data
center — Musk's pivot to compute provider (see
[AI infrastructure](ai-infrastructure-compute-energy.md)). The show's first "AI Lab
Power Rankings" (Apr 2026) placed Google first by aggregated model self-scoring.

## US–China race and "data center diplomacy"

The geopolitical thread spans chip export controls (the [AI Diffusion Rule](ai-infrastructure-compute-energy.md),
its rescission, H200-to-China for a 25% cut, proposed Blackwell bans), Chinese
open-weight models (DeepSeek V4, GLM 5.2, Kimi) positioned as "good enough at a
fraction of the cost," and "data center diplomacy" via the UAE/G42 as a neutral third
pole. DeepSeek R1's ~$600B single-day NVIDIA loss is the recurring symbol of the
China threat.

## AI becomes political

By 2026 the domestic politics sharpened: after Anthropic refused to drop
prohibitions on domestic mass surveillance and autonomous weapons, the Pentagon
moved to designate it a "supply chain risk" and the administration directed agencies
to phase out its technology — the same week OpenAI announced its own DoD deal. The
government effectively became an informal frontier-model licensing authority
(delaying GPT-5.6 to a partner preview), while open-weight models (Gemma 4 at 200M
downloads) gained momentum. The ownership question — whether the public should hold
equity (Sanders' fund act; OpenAI's and Anthropic's own endorsements) — closes the
loop with [AI economics](ai-economics-and-the-bubble-debate.md).

## Open questions

- **Third-hand and single-source**: this is one host's (Nathaniel Whittemore's)
  analysis as relayed in owner's notes; framings reflect his presentation, not
  independent reporting. Verify before promoting past `draft`/`medium`.
- Many 2026 events (lab power rankings, the "ad hoc licensing regime," specific deal
  terms) are recent, fast-moving, and unverified from this corpus.
- Legal/policy specifics (statute citations, export-cap numbers) are as-reported and
  should be checked against primary documents.

## Sources

- `sources/audio/2026-01-03-what-manus-and-groq-acquisitions-tell-us-about-ai.md` — Meta–Manus, NVIDIA–Groq (`meta-manus-nvidia-groq-2026-acquisitions`)
- `sources/audio/2026-04-29-ai-lab-power-rankings.md` — MSFT/OpenAI amendment, lab rankings (`microsoft-openai-2026-amendment-terms`, `ai-lab-power-rankings-google-first`)
- `sources/audio/2026-02-11-how-the-global-ai-race-has-shifted.md` — DeepSeek loss, G42 diplomacy, export politics (`deepseek-r1-nvidia-600b-loss`)
- `sources/audio/2026-02-28-who-controls-ai.md` — Anthropic–Pentagon SCR designation (`anthropic-pentagon-scr-designation`)
- `sources/audio/2026-03-06-ai-is-officially-political.md` — OpenAI DoD deal, "safety theater" memo (`openai-dod-deal-same-day`)
- `sources/audio/2026-06-27-the-ad-hoc-ai-licensing-regime-ai-weekly-brief.md` — ad hoc licensing, Gemma 4 (`ad-hoc-licensing-gpt56`)
- `sources/audio/2026-05-07-surprise-elon-anthropic-team-up-reshapes-the-ai-race.md` — Anthropic leases xAI Colossus (`elon-anthropic-colossus-lease`)
- `sources/audio/2026-04-16-ai-s-great-divergence.md` — PwC top-20% gains (`pwc-75-percent-gains-top-20`)
- `sources/audio/2026-04-27-how-deepseek-v4-connects-to-the-us-power-grid.md` — Google $40B, China blocks Manus (`google-40b-anthropic-china-blocks-manus`)
- `sources/audio/2025-05-03-nvidia-and-anthropic-trade-barbs-around-ai-chip-rules.md` — AI Diffusion Rule (`ai-diffusion-rule-tiers`)
- `sources/audio/2025-05-31-nvidia-ceo-says-china-ai-is-catching-up-fast.md` — Saudi Humane sovereign compute (`saudi-humane-infrastructure`)
- `sources/audio/2025-12-10-the-ai-race-gets-a-massive-power-shift.md` — H200-to-China, compute advantage (`trump-h200-china-25pct-cut`, `compute-advantage-33-to-1`)
- `sources/audio/2025-12-10-the-state-of-enterprise-ai.md` — Anthropic overtakes OpenAI in enterprise spend (`anthropic-enterprise-share-40`)
- `sources/audio/2026-06-02-should-americans-get-shares-in-ai-companies.md` — Sanders sovereign-wealth-fund act (`sanders-sovereign-wealth-fund-act`)
- `sources/audio/2026-02-06-opus-4-6-and-chatgpt-5-3-codex-are-here-and-the-labs-are-at.md` — near-simultaneous launches (harness rivalry) (`opus46-gpt53-simultaneous`)
