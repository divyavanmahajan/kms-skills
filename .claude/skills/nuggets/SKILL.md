---
name: nuggets
description: Extract nuggets (claim-level evidence units with context and provenance, richer than chunks) from a source into nuggets/<slug>.yaml. Use when a source lacks a nugget file, when the user says "nuggetize" or "extract nuggets/claims", or as part of ingestion.
---

# Extract nuggets from a source

Follow `AGENTS.md` and `policies/nugget-policy.md` (read it — it defines the
schema and the context rule). Nuggets are the claim inventory between
`sources/` and `wiki/`.

## Input

`$ARGUMENTS` names one or more files under `sources/`. If empty, find sources
without a matching `nuggets/<slug>.yaml` and process those.

## Procedure

1. Read the source in full, including its frontmatter (`type:` caps
   confidence: `summary-notes` → at most `medium`).
2. Identify every claim the citation policy would require a source for:
   technical claims, comparisons, numbers/benchmarks/prices, version-specific
   statements, notable direct quotes. Skip navigation text and pure opinion
   (or record opinion with `context` saying whose opinion it is).
3. For each claim, write a nugget:
   - `claim` — one atomic, self-contained sentence or two. No dangling
     "it/this"; name the systems, people, versions.
   - `context` — who says so (vendor claim? independent measurement? author
     opinion?), when (absolute dates/versions), and scope. The test: claim +
     context must be fully interpretable without opening the source.
   - `quote` — optional short verbatim anchor for the most load-bearing wording.
   - `id` — globally unique kebab-case; check collisions:
     `grep -rh "id:" nuggets/`.
4. Write `nuggets/<same-slug-as-source>.yaml`. One file per source; if the
   file exists, append new nuggets — never reword existing `claim` fields
   (corrections supersede: new nugget + `status: superseded` on the old).
5. Cross-check the new claims against existing nuggets (`grep` key terms in
   `nuggets/`): incompatible claims about the same fact → mark BOTH
   `status: disputed` and flag in your report (the `contradictions` skill's
   classification applies).
6. `python3 scripts/lint.py` (validates nugget schema and id uniqueness), then
   `python3 scripts/dashboard.py`.
7. Commit as `ingest: nuggets for <source>` (medium risk — branch/PR unless
   told otherwise).

## Report

Nugget count per source, any disputes raised, and which wiki pages could now
cite specific nugget ids.
