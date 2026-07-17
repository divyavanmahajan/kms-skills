---
title: Long-term maintenance guidelines
status: draft
confidence: medium
created: 2026-07-17
review_after: 2027-01-13
review_interval_days: 180
sources:
  - sources/web/2026-07-17-what-is-llm-wiki.md
  - sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md
tags: [maintenance, guidelines, governance]
---

# Long-term maintenance guidelines

## Summary

The operating guidelines for keeping this knowledge base healthy over years,
distilled from the two glukhov.org articles this repo is built on: *What is an
LLM Wiki* (architecture) and *LLM Wiki maintenance & knowledge drift*
(operations). Each guideline is traced to its source article and to the
concrete mechanism implementing it in this repository. The
[coverage check](#coverage-check) at the end confirms what is implemented and
what is deliberately not (yet).

Article key used below: **[A1]** = `sources/web/2026-07-17-what-is-llm-wiki.md`,
**[A2]** = `sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md`.

## 1. Architecture and format

**G1 — Compile at ingest time; preserve synthesis, don't regenerate it per
query.** [A1] The wiki's value is reusable, reviewed synthesis.
*Here:* the `/ingest` skill compiles sources into `wiki/` pages once;
[nuggets](../topics/nuggets.md) capture the claim inventory at the same moment.

**G2 — Use boring formats: plain Markdown in Git.** [A1] "Boring formats
survive longer than clever platforms" — the system must stay inspectable,
diffable, portable.
*Here:* everything is Markdown + YAML in a Git repo; the web UI (MkDocs) and
any editor (see the [Obsidian guide](obsidian.md)) are replaceable layers on top.

**G3 — Never replace originals; generated pages sit above sources.** [A1][A2]
Summaries can be regenerated; lost sources cannot.
*Here:* `sources/` is append-only (`policies/source-policy.md`); AGENTS.md
prime directive 1 forbids edits; retrieval dates and `type:` are mandatory
frontmatter.

**G4 — Prefer fewer, better pages; update instead of adding.** [A1][A2]
Over-structuring and page proliferation are failure modes (structure drift).
*Here:* the `/ingest` skill requires searching for an existing page first;
`schema.md` caps pages at one concept (~300 lines); `lint.py` flags orphans.

## 2. Provenance and honesty

**G5 — Every important claim links back to its sources.** [A1][A2] "Generated
structure needs provenance"; a compiled summary "has to be actively kept honest."
*Here:* `sources:` frontmatter + per-page *Sources* section
(`policies/citation-policy.md`); claim-level traceability via nugget ids
(`policies/nugget-policy.md`); `lint.py` errors on nonexistent source paths.

**G6 — Mark uncertainty explicitly rather than hiding it.** [A1] Use status
indicators like "disputed" / "needs review."
*Here:* `status: draft|reviewed|disputed|superseded` and
`confidence: low|medium|high` are required frontmatter; unsourced claims must
move to *Open questions*, never be silently deleted.

**G7 — Re-verify citations after every rewrite (citation drift).** [A2] A claim
that no longer matches its citation creates "false confidence."
*Here:* the `/review` skill's step 2 re-checks each claim against listed
sources; `review-policy.md` requires a citation check before any
`draft → reviewed` promotion. Nugget claims are immutable, so drift between a
claim and its record is impossible by construction.

## 3. Change discipline

**G8 — Human review is non-negotiable; LLMs draft, humans approve.** [A1][A2]
*Here:* risk tiers in `review-policy.md`/`AGENTS.md` — agents commit only
low-risk fixes directly; medium/high risk goes to PRs that only the owner
merges; the weekly CI session is explicitly forbidden from merging.

**G9 — Keep agent changes small and reviewable as Git diffs.** [A2] "Avoid
agent rewrites larger than necessary"; commit messages explain operations.
*Here:* AGENTS.md prime directive 4 (small diffs) and the commit prefix
convention (`ingest:`, `review:`, `lint:`, `dashboard:`, `policy:`).

**G10 — Supersede, never delete; link forward.** [A2] History must stay
recoverable; superseded pages point to replacements.
*Here:* `status: superseded` + `superseded_by` for pages **and** nuggets;
`lint.py` errors when a superseded item lacks a valid replacement link.

**G11 — Be able to roll back any bad update.** [A2] "Can we roll back a bad
update?" is a test the system must always pass.
*Here:* Git — every change is a commit; `git revert` restores any prior state;
the append-only sources layer guarantees evidence survives even a bad rollback.

**G12 — Record decisions with an explicit lifecycle status.** [A2] Decision
drift: superseded decisions documented as current practice.
*Here:* `wiki/decisions/` records with `draft` (proposed) / `reviewed`
(accepted) / `superseded` status per `schema.md`; the `/review` skill checks
pages against decision records.

## 4. Drift countermeasures

**G13 — Automate structural checks; they validate maintainability, not
truth.** [A2] Broken links, orphans, missing metadata, inconsistent naming.
*Here:* `scripts/lint.py`, run on every push (`.github/workflows/lint.yml`)
and in the weekly loop.

**G14 — Semantic checks flag, they never auto-rewrite.** [A2] Unsourced
claims, incompatible pages, outdated decisions need judgment.
*Here:* the `/review` skill marks pages `disputed`/stale and routes claim
changes through PRs; nothing semantic is changed by deterministic scripts.

**G15 — Detect contradictions by comparing claims, then classify before
resolving.** [A2] Actual contradiction vs. version difference vs. scope
difference; valid resolutions include preserving the disagreement.
*Here:* the `/contradictions` skill runs over the `nuggets/` claim inventory;
both conflicting nuggets/pages become `disputed` until a human resolves.

**G16 — Fight terminology drift with a canonical glossary and recorded
aliases.** [A2] Multiple names for one concept break search and linking.
*Here:* [glossary](../glossary.md) records aliases explicitly (e.g. *nugget* =
Microsoft's "structured evidence object"); skills are instructed to add
aliases rather than rename historical content.

**G17 — Split canonical content from version-specific content.** [A2]
*Here:* `schema.md` rule — version-specific claims go in labelled sections or
their own pages; nugget `context` must carry version/date scope.

## 5. Cadences, metrics, ownership

**G18 — Review on a schedule, tiered by how fast content decays.** [A2]
Pricing 7–30 days; tool pages 30–90; principles 6–18 months; historical
records only when superseded.
*Here:* `review_after`/`review_interval_days` frontmatter with the
`review-policy.md` interval table; the dashboard lists overdue pages; the
weekly Action reviews the most overdue ones.

**G19 — Track health with a small set of metrics on a working dashboard.**
[A2] Page counts, sourced vs. unsourced, past-due pages, broken links,
orphans, stale percentage — "Markdown dashboards ... without engineering
overhead."
*Here:* `scripts/dashboard.py` regenerates [the dashboard](../dashboard.md)
weekly (CI) and after every skill run.

**G20 — Someone must own the system.** [A1] Ownership ambiguity is a decay
mode: without clear responsibility, systems rot.
*Here:* single-owner repo — the owner merges every medium/high-risk PR, which
makes ownership structural rather than aspirational. If this ever becomes a
team repo, add per-page `owner:` frontmatter (see coverage check).

## Coverage check

Every maintenance concept found in the two articles, and where it landed:

| # | Concept | Article | Implementation | Status |
|---|---------|---------|----------------|--------|
| G1 | Ingest-time compilation | A1 | `/ingest` skill, `wiki/` layer | ✅ |
| G2 | Markdown / boring formats | A1 | Whole repo; MkDocs on top | ✅ |
| G3 | Source preservation | A1, A2 | `sources/` append-only + `source-policy.md` | ✅ |
| G4 | Fewer better pages, no over-structuring | A1, A2 | Update-first rule, orphan lint | ✅ |
| G5 | Provenance on every claim | A1, A2 | `sources:` frontmatter, nuggets, lint | ✅ |
| G6 | Uncertainty marking | A1 | `status` + `confidence` fields | ✅ |
| G7 | Citation-drift checks | A2 | `/review` step 2; pre-promotion check | ✅ |
| G8 | Human review / approval | A1, A2 | Risk tiers; PR-only medium/high | ✅ |
| G9 | Small diffs + commit conventions | A2 | AGENTS.md rules | ✅ |
| G10 | Supersede, don't delete | A2 | `superseded_by` + lint enforcement | ✅ |
| G11 | Rollback capability | A2 | Git history / revert | ✅ |
| G12 | Decision records with status | A2 | `wiki/decisions/` | ✅ |
| G13 | Structural linting | A2 | `lint.py` + CI on push | ✅ |
| G14 | Semantic checks flag-only | A2 | `/review` skill | ✅ |
| G15 | Contradiction detection & classification | A2 | `/contradictions` + nugget inventory | ✅ |
| G16 | Glossary / alias management | A2 | `wiki/glossary.md` | ✅ |
| G17 | Canonical vs. version-specific split | A2 | `schema.md` rule | ⚠️ policy only — no lint check |
| G18 | Tiered review intervals | A2 | Frontmatter + weekly staleness review | ✅ (weekly, stricter than the article's monthly) |
| G19 | Health metrics dashboard | A2 | `dashboard.py` → `wiki/dashboard.md` | ✅ |
| G20 | Clear ownership | A1 | Single owner merges all PRs | ⚠️ implicit — no per-page `owner:` field |
| G21 | Hybrid with RAG (wiki + retrieval layer over the same sources) | A1 | — | ❌ not implemented — MkDocs full-text search only; noted as a future extension |

**Known gaps, on purpose:** G17 needs a human eye (a lint heuristic would
misfire); G20 is unnecessary overhead for a single-owner repo; G21 (a RAG
layer over `sources/`) is a real extension candidate if the corpus outgrows
browsing and search.

## Sources

- `sources/web/2026-07-17-what-is-llm-wiki.md` — G1–G6, G8, G20, G21
  (architecture, principles, roles, failure modes)
- `sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md` — G3–G5,
  G7–G19 (drift taxonomy, operating files, tiers, cadences, metrics;
  nuggets: `drift-six-mechanisms`, `drift-compiled-must-be-kept-honest`,
  `drift-review-intervals`, `drift-citation-false-confidence`)
