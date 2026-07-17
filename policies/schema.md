# schema.md — Page Structure Policy

Every Markdown file under `wiki/` (except generated files: `dashboard.md`) MUST
follow this schema so agents can update pages predictably and scripts can lint them.

## Frontmatter

```yaml
---
title: Human-readable title
status: draft            # draft | reviewed | disputed | superseded
confidence: medium       # low | medium | high
created: 2026-07-17
reviewed: 2026-07-17     # date of last human review (omit until first review)
review_after: 2026-10-15 # page counts as stale after this date
review_interval_days: 90 # used to bump review_after on each review
sources:                 # repo-relative paths; may be empty ONLY for status: draft
  - sources/web/2026-07-17-example.md
superseded_by: topics/replacement.md  # REQUIRED when status: superseded (wiki-relative)
tags: [example]
---
```

Required keys: `title`, `status`, `confidence`, `review_after`, `sources`.

### Status meanings

- **draft** — compiled by an agent, not yet human-reviewed. May be unsourced.
- **reviewed** — a human verified claims against sources on the `reviewed` date.
- **disputed** — a contradiction or doubt is recorded; see the page's *Open questions*.
- **superseded** — kept for history; `superseded_by` points to the replacement.

## Page types and required sections

### Topic page (`wiki/topics/`)

```markdown
## Summary
2–5 sentences. What a reader needs if they read nothing else.

## <Content sections...>
Free-form, but small and focused. Link related topics inline.

## Open questions
Unresolved doubts, unsourced claims, known disputes. Omit if none.

## Sources
- `sources/web/...` — what this source supports (one line each)
```

### Decision record (`wiki/decisions/`)

Named `NNNN-short-title.md`. Sections: `## Context`, `## Decision`,
`## Consequences`. The frontmatter `status` doubles as the decision status —
decisions use `draft` (proposed), `reviewed` (accepted), `superseded`.

### Glossary (`wiki/glossary.md`)

One `## Term` heading per term, definition below it, linking to the owning topic
page. Record synonyms/aliases explicitly ("also called ...") to fight
terminology drift.

## Rules

- File names: `kebab-case.md`.
- Review intervals by content type are set in [`review-policy.md`](review-policy.md).
- One concept per page. If a page grows past ~300 lines, split it and cross-link.
- Version-specific claims go in a clearly-labelled section or their own page —
  never mixed silently into canonical/timeless content.
