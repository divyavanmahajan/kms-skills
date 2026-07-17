---
url: https://commandline.microsoft.com/grounding-system-agentic-web-engineering-retrieval/
retrieved: 2026-07-17
type: summary-notes
---

# Grounding at scale: engineering the retrieval system for the agentic web (Microsoft Command Line blog) — summary notes

Engineering companion to the Web IQ announcement. Key material on evidence
objects (the passage-level retrieval units).

## Evidence objects

Defined as "passage-level units with provenance, structural metadata, and
enough local context to remain interpretable when detached from the source
page."

Composition:
- provenance (attribution back to the source)
- structural metadata
- sufficient surrounding local context to stand alone off-page

## Difference from plain chunks

- Optimization target changes from **document relevance** to **information
  density per token**.
- Aim: "preserve the evidence needed for reasoning without paying the token
  cost of full-document recall."
- Better evidence objects: reduce prompt size, improve reasoning quality by
  concentrating relevant facts, and preserve attribution so outputs remain
  inspectable.
- Passages are selected for information density relative to the query, not the
  document's overall relevance.

## Pipeline position

Evidence objects are produced in the orchestration layer's
context-construction phase: after retrieval yields candidates from the
semantic index, a component selects and packages evidence for model
consumption under strict latency and context-window constraints.

## Stack notes

In a semantic-first stack, dense retrieval is the default access path; later
stages recover precision through richer interaction, filtering, calibration,
and task-specific refinement. That choice propagates into how content is
chunked, how representations are trained, and what the ANN index must
preserve. The article frames evidence objects as practical token-economics
optimization rather than architectural novelty, and gives minimal structural
specification beyond the functional role.
