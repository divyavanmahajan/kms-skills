---
name: contradictions
description: Sweep the wiki for contradictions between pages — conflicting claims, incompatible definitions, decisions documented as current but superseded elsewhere. Classify each conflict and propose resolutions. Use monthly, after large ingests, or when the user suspects inconsistency.
---

# Contradiction sweep

Follow `AGENTS.md`. Detection is the job; resolution beyond low-risk fixes goes
to a PR for human judgment.

## Procedure

1. Build a claim inventory: start from `nuggets/` (the structured claim
   inventory — non-superseded nuggets only). For wiki pages whose sources have
   no nugget file yet, extract claims from the page prose (and consider
   running the `nuggets` skill to backfill).
2. Group claims by concept — use the glossary to catch synonym pairs
   (terminology drift hides contradictions).
3. For each group with more than one page, compare claims and classify conflicts:
   - **Actual contradiction** — both can't be true.
   - **Version/time difference** — both were true at different times or versions.
   - **Scope difference** — true in different contexts, stated too generally.
   - **Terminology mismatch** — same fact, different words; not a real conflict.
4. For every real finding, check the cited sources before judging — the page may
   have drifted from its source rather than from the other page.

## Resolutions

- Actual contradiction → mark BOTH pages `status: disputed`, record positions +
  citations in *Open questions*, propose the resolution in a PR.
- Version/time → mark the older page `superseded` (with `superseded_by`), or
  split version-specific claims into labelled sections/pages.
- Scope → narrow the over-general statement, citing both sources.
- Terminology → add aliases to `wiki/glossary.md` and normalize links (low
  risk — commit directly).
- Preserving a genuine expert disagreement (sources disagree) is a valid
  outcome: present both views with citations, `confidence: low`.

## Finish

`python3 scripts/lint.py`, `python3 scripts/dashboard.py`, commit as
`review: contradiction sweep — <n> findings`. Report findings in a table:
pages, claim, classification, proposed resolution.
