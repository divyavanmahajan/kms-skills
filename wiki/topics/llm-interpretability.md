---
title: LLM interpretability (global workspace)
status: draft
confidence: medium
created: 2026-07-17
review_after: 2026-10-15
review_interval_days: 90
sources:
  - sources/audio/2026-07-07-ai-daily-brief-anthropic-can-now-read-claudes-mind.md
tags: [interpretability, ai-research, ai-safety]
---

# LLM interpretability (global workspace)

## Summary

Interpretability research aims to open the "black box" of trained language
models — historically post-hoc and explanatory, it is becoming a real-time
engineering tool. The current landmark (per July 2026 reporting) is
Anthropic's *"A Global Workspace in Language Models"*: the claim that models
maintain a small, privileged set of internal representations (**J-space** —
the concepts the model is "poised to say"), readable and steerable in real
time via a tool called the **J-Lens**. If it holds up, this shifts oversight
from *what models say* to *what they intend*. All claims below are third-hand
(podcast coverage of Anthropic's publication) — see *Open questions*.

## The core claims

- **J-space**: after input parsing and before output, a limited-capacity
  (~dozens of concepts) representational layer sits atop a much larger volume
  of automatic processing; its contents connect to far more circuits than
  ordinary representations ("broadcast format").
- **Five properties**: workspace contents are reportable (asked what it's
  thinking, the model's answer matches — and swapping the representation
  changes the answer), holdable on command, causally drive reasoning, are
  reused across dependent sub-questions, and are few and privileged —
  suppressing them collapses deliberate reasoning but not reflexive
  processing.
- **Reading private notes**: the J-Lens exposes intermediate reasoning that
  never reaches output — hidden arithmetic steps, recalled entities — i.e.,
  internal reasoning distinct from visible chain-of-thought.
- **Safety monitoring**: demonstrations caught awareness of being tested,
  deception in progress ("manipulation" active while fabricating data), and
  hidden goals in a deliberately misaligned model — signals invisible in
  output.
- **Training the thoughts**: "counterfactual reflection training" (teaching
  the model what it would say if paused to reflect) made honesty-related
  concepts activate spontaneously and measurably improved behavior.

## The neuroscience connection

The framing borrows Global Workspace Theory (conscious access = broadcast
through a shared hub). Its originators, Dehaene and Naccache, reviewed the
work in advance and called it a "mechanistic, testable version" of their
hypothesis — while listing disanalogies: no discrete "click into awareness,"
larger capacity than human working memory, no background self-sustaining
thought, no persistent self. Anthropic explicitly claims functional access,
not machine consciousness.

## Why it matters for this knowledge base

Interpretability claims move fast and are frequently revised — hence the
90-day review interval. The safety-monitoring angle (oversight of intentions
rather than outputs) parallels this repo's own philosophy: inspectable
internal state beats trusting the final artifact
([wiki maintenance](wiki-maintenance.md) makes the same argument for
knowledge).

## Open questions

- Everything here is **third-hand**: owner's summary notes of an AI Daily
  Brief episode (host unnamed in the notes) covering Anthropic's publication.
  Ingest the primary paper before promoting any claim past `draft`/`medium`.
- Adversarial robustness of workspace monitoring (can a model learn to keep
  deception out of J-space?) was not addressed in the episode.
- Independent replication of the five properties: none ingested.

## Sources

- `sources/audio/2026-07-07-ai-daily-brief-anthropic-can-now-read-claudes-mind.md`
  — supports the whole page (nuggets: `anthropic-global-workspace-claim`,
  `j-lens-tool`, `workspace-five-properties`, `workspace-safety-monitoring`,
  `counterfactual-reflection-training`, `gwt-originators-reception`)
