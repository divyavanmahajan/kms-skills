# AGENTS.md — Operating Rules for Agents

Any agent (Claude Code, CI-driven Claude sessions, or other LLM tooling) working in
this repository MUST follow these rules. They exist to prevent knowledge drift and to
keep every change inspectable and recoverable.

## The prime directives

1. **Never edit `sources/`.** Raw sources are append-only. You may ADD new source
   files (via ingestion) but never modify or delete existing ones. The single
   sanctioned exception is an **owner-requested retraction** via the
   `remove-source` skill: it removes sources *and* all derived content, records
   the removal in the append-only `sources/RETRACTIONS.md` log, and goes
   through a PR. Never retract on your own initiative.
2. **Supersede, don't delete.** Wiki pages are never deleted. Mark them
   `status: superseded`, set `superseded_by`, and link forward. The same goes
   for nuggets in `nuggets/`: a recorded `claim` is never reworded — correct it
   with a new nugget that supersedes the old one
   ([`policies/nugget-policy.md`](policies/nugget-policy.md)).
3. **Every claim needs provenance.** Follow [`policies/citation-policy.md`](policies/citation-policy.md).
   If you cannot source a claim, mark the page `confidence: low` and add it to
   *Open questions* — do not state it as fact.
4. **Small diffs beat rewrites.** Update the smallest section that needs changing.
   Never rewrite a whole page when a paragraph edit suffices.
5. **Lint before you commit.** Run `python3 scripts/lint.py` and fix errors before
   any commit that touches `wiki/`.

## Risk tiers (from policies/review-policy.md)

| Tier | Examples | Agent may... |
|------|----------|--------------|
| Low | Link fixes, typos, formatting, tag/alias updates, dashboard regeneration | Commit directly |
| Medium | New topic pages, new summaries, updated recommendations, glossary entries | Commit on a branch / open a PR |
| High | Deleting or superseding claims, changing canonical pages, security/pricing/version claims, editing policies | Open a PR and explicitly flag for human approval — never merge |

When in doubt, treat the change as one tier higher.

## Commit message conventions

Prefix commits with the operation so history is scannable:

- `ingest: <what was added>` — new source + compiled/updated pages
- `review: <page> <outcome>` — semantic review results (bumped review date, marked disputed, superseded)
- `lint: <fix>` — structural fixes (links, metadata, naming)
- `dashboard: regenerate` — generated dashboard updates
- `policy: <change>` — changes to files in `policies/` (high risk, PR only)
- `retract: <what was removed>` — owner-requested source removal + derived-content
  cleanup via the `remove-source` skill (high risk, PR only)

## The maintenance loop

The repeatable loop every maintenance session follows:

1. Add / detect new sources (`inbox/` and `sources/`)
2. Extract nuggets (claim inventory) per [`policies/nugget-policy.md`](policies/nugget-policy.md),
   then compile: create or update wiki pages per [`policies/schema.md`](policies/schema.md)
3. Update links between pages
4. Structural lint: `python3 scripts/lint.py`
5. Semantic review: check stale pages (see `wiki/dashboard.md`) against their sources
6. Human approval for medium/high-risk changes (PR)
7. Commit with conventional messages
8. Regenerate the dashboard: `python3 scripts/dashboard.py`

## Page hygiene

- Follow the frontmatter and section schema in [`policies/schema.md`](policies/schema.md) exactly.
- File names are `kebab-case.md`.
- Prefer updating an existing page over creating a near-duplicate. Search first:
  `grep -ri "<concept>" wiki/`.
- When two pages conflict, do not silently pick a winner. Classify the conflict
  (actual contradiction vs. version/scope difference) and either mark one page
  superseded, split version-specific content out, or record the disagreement
  explicitly with both sources cited.
- Distinguish decisions from facts: decisions live in `wiki/decisions/` with a
  status of `proposed | accepted | superseded`.
- **Bulk ingest (a directory / many similar files):** never one page per
  source and never regex-scraped nuggets. Preserve all sources first (a script
  may do this — copy the frontmatter shape of an existing example or reuse
  `scripts/fetch_notes.py`; dedup by `guid`), then compile a *small* set of
  cross-cutting themed pages, with nuggets extracted by *reading* (fan out
  subagents at volume). See the `ingest` skill's "Bulk ingest" section. This
  holds regardless of which model runs it.
