---
title: "0001: Repository architecture"
status: reviewed
confidence: high
created: 2026-07-17
reviewed: 2026-07-17
review_after: 2031-07-16
sources:
  - sources/web/2026-07-17-what-is-llm-wiki.md
  - sources/web/2026-07-17-llm-wiki-maintenance-knowledge-drift.md
tags: [decision]
---

# 0001: Repository architecture

## Context

We want a self-managed knowledge system following the compiled-knowledge
("[LLM wiki](../topics/llm-wiki.md)") architecture: sources preserved,
knowledge compiled with provenance, drift actively managed. It must be usable
by one person, automatable, and browsable on the web.

## Decision

One repository containing both the toolkit and the live wiki:

- **Format**: plain Markdown in Git — inspectable, diffable, recoverable.
- **Layout**: `sources/` (append-only raw material), `wiki/` (compiled pages),
  `inbox/` (drop zone), `policies/` (operating rules), `scripts/`
  (deterministic checks), `.claude/skills/` (LLM judgment work).
- **LLM layer**: Claude Code skills (`/ingest`, `/review`, `/contradictions`,
  `/maintain`) for synthesis and semantic review; humans approve
  medium/high-risk changes via PRs.
- **Deterministic layer**: Python scripts for structural lint and the health
  dashboard — never LLM calls for what a script can check.
- **Web UI**: MkDocs Material published to GitHub Pages from `main`
  (read-only; editing happens through Git).
- **Automation**: GitHub Actions — lint on every push, weekly dashboard
  regeneration, and a scheduled Claude maintenance session that opens PRs.

## Consequences

- Everything is reviewable as Git diffs; bad updates roll back with `git revert`.
- The wiki is portable: no database, no proprietary platform.
- Maintenance depends on the weekly Action and on the owner reviewing PRs;
  ignoring maintenance PRs lets [drift](../topics/knowledge-drift.md) accumulate.
- The scheduled Claude session requires an `ANTHROPIC_API_KEY` repo secret and
  incurs API costs weekly.
