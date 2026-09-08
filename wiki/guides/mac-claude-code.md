---
title: Using the KMS on Mac with Claude Code
status: draft
confidence: high
created: 2026-09-08
review_after: 2026-12-07
review_interval_days: 90
sources: []
tags: [guide, mac, claude-code, tooling, walkthrough]
---

# Using the KMS on Mac with Claude Code

## Summary

This walkthrough sets up the knowledge system on macOS with **Claude Code**,
which is the first-class client for this repo: the skills (`/ingest`,
`/review`, `/maintain`, …) run as slash commands, the `kms` knowledge-graph
MCP server loads automatically from `.mcp.json`, and `CLAUDE.md`/`AGENTS.md`
are picked up as project instructions.

> **Maintenance note:** if you add or change a user-facing feature (a skill, a
> script, an MCP tool, a setup step), update this walkthrough and
> [the Windows + Copilot one](windows-github-copilot.md) in the same change —
> see the walkthrough rule in `AGENTS.md`.

## Prerequisites

- **Command Line Tools / git** — `xcode-select --install` (or Homebrew's git)
- **Python 3.11+** — macOS ships one; `brew install python` for current
- **Claude Code** — `npm install -g @anthropic-ai/claude-code` (or
  `brew install --cask claude-code`), then run `claude` once to log in

## 1. Clone and install

```bash
git clone https://github.com/divyavanmahajan/kms-skills.git
cd kms-skills
python3 -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt -r requirements-mcp.txt
```

## 2. Build the knowledge-graph index

```bash
python3 -m kms_mcp index          # one-time; downloads the ~90MB embedding model once
python3 -m kms_mcp search "enterprise AI adoption"   # sanity check
```

## 3. Start Claude Code

```bash
claude
```

On first run in the repo, approve the `kms` MCP server when prompted (it's
defined in `.mcp.json`; check it with `/mcp`). If you use a venv, start
`claude` from the activated shell so `python3 -m kms_mcp` resolves to the venv
with the dependencies installed.

Now just talk to the knowledge base:

> *What does the KB say about enterprise agent adoption? Cite nugget ids.*

> *Show everything connected to Nvidia in the knowledge graph.*

Claude uses `kms_semantic_search`, `kms_graph_query`, `kms_related`, and
`kms_get_document` under the hood (per `CLAUDE.md` it prefers these over
grep for knowledge questions).

## 4. The skills

| Command | What it does |
|---|---|
| `/ingest <url\|file>` | snapshot a source, extract nuggets + entities, compile wiki pages |
| `/ingest-audio <file>` | audio/podcast variant (asks for metadata, transcribes) |
| `/nuggets [source]` | extract claim-level nuggets from a source |
| `/review [page]` | semantic review of stale/flagged pages |
| `/contradictions` | contradiction sweep across nuggets + pages |
| `/remove-source <glob>` | retract sources and everything derived from them |
| `/maintain` | the full weekly maintenance loop |

Everything follows `AGENTS.md` (append-only sources, supersede don't delete,
citations, risk tiers, commit prefixes, **no AI attribution in commits**).
After content changes, Claude reindexes via `kms_reindex` or
`python3 -m kms_mcp index`.

## 5. Optional: HTTP mode for other agents

To let other local agents or clients use the same server:

```bash
python3 -m kms_mcp serve --http --port 8471    # http://127.0.0.1:8471/mcp
```

Bind beyond localhost only behind your own auth/reverse proxy — the server
itself does no authentication.

## Sources

Setup steps verified against this repo's tooling as of 2026-09; Claude Code
install/UI steps may drift with new releases — re-verify on major Claude Code
updates.
