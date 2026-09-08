---
title: Using the KMS on Windows with GitHub Copilot
status: draft
confidence: high
created: 2026-09-08
review_after: 2026-12-07
review_interval_days: 90
sources: []
tags: [guide, windows, copilot, tooling, walkthrough]
---

# Using the KMS on Windows with GitHub Copilot

## Summary

This walkthrough sets up the knowledge system on Windows with **VS Code +
GitHub Copilot** as the assistant. Copilot gets the same knowledge-graph and
semantic-search tools Claude uses (via the `kms` MCP server, wired up in
`.vscode/mcp.json`) and the same operating rules (via
`.github/copilot-instructions.md`, which points at `AGENTS.md`). The
Claude-specific skills (`/ingest`, `/maintain`, …) don't run as slash commands
in Copilot, but their procedures are plain Markdown you can hand to Copilot as
instructions.

> **Maintenance note:** if you add or change a user-facing feature (a skill, a
> script, an MCP tool, a setup step), update this walkthrough and
> [the Mac + Claude Code one](mac-claude-code.md) in the same change — see the
> walkthrough rule in `AGENTS.md`.

## Prerequisites

- **Git for Windows** — <https://git-scm.com/download/win>
- **Python 3.11+** — <https://python.org/downloads> (check *"Add python.exe to
  PATH"* during install; verify with `python --version` in a new terminal)
- **VS Code** with the **GitHub Copilot** and **GitHub Copilot Chat**
  extensions, signed in to a Copilot-enabled GitHub account

## 1. Clone and install

In PowerShell:

```powershell
git clone https://github.com/divyavanmahajan/kms-skills.git
cd kms-skills
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-mcp.txt
```

(If activation is blocked, run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and retry.)

## 2. Build the knowledge-graph index

```powershell
python -m kms_mcp index
```

First run downloads the ~90MB embedding model once into `.kms-index/models`;
afterwards everything is offline. Quick check:

```powershell
python -m kms_mcp search "enterprise AI adoption"
```

## 3. Give Copilot the knowledge-graph tools (MCP)

The repo ships `.vscode/mcp.json`, which registers the `kms` MCP server for VS
Code. Open the repo folder in VS Code (with the `.venv` selected as the Python
interpreter, or the venv activated in the terminal VS Code uses), then:

1. Open **Copilot Chat** and switch the mode picker to **Agent**.
2. VS Code will show the MCP server from `.vscode/mcp.json` and ask you to
   **trust/start** it — accept. (If it doesn't appear, make sure MCP support
   is enabled: Settings → search "mcp" → *Chat: MCP* enabled, then run
   **MCP: List Servers** from the command palette and start `kms`.)
3. In the tools picker you should now see `kms_semantic_search`,
   `kms_graph_query`, `kms_related`, `kms_get_document`, `kms_graph_schema`,
   and `kms_reindex`.

Try it:

> *What does the knowledge base say about enterprise agent adoption? Use the
> kms tools, and cite the nugget ids.*

> *Show me everything connected to Nvidia in the knowledge graph.*

## 4. Working by the repo's rules

Copilot reads `.github/copilot-instructions.md`, which summarizes the
operating rules and points to `AGENTS.md` (append-only sources, supersede
don't delete, citation requirements, risk tiers, commit prefixes, **no AI
attribution in commits**). For the bigger judgment workflows, the Claude skill
procedures under `.claude/skills/` are plain Markdown — use them as
instructions, e.g.:

> *Follow the procedure in `.claude/skills/ingest/SKILL.md` to ingest the file
> `inbox/note-....md`.*

Deterministic checks run the same as anywhere:

```powershell
python scripts\lint.py            # before every commit touching wiki/
python scripts\dashboard.py
python scripts\extract_entities.py --check
python -m kms_mcp index           # after content changes
```

## What's different from Claude Code

- **Skills aren't slash commands** — reference the `SKILL.md` files manually
  (above).
- `.mcp.json` (repo root) is Claude's MCP config; `.vscode/mcp.json` is the
  one VS Code/Copilot uses. They point at the same server.
- Scheduled maintenance still happens in GitHub Actions regardless of which
  editor you use.

## Sources

Setup steps verified against this repo's tooling; VS Code/Copilot UI steps
reflect VS Code's MCP support as of 2026-09 and may drift — re-verify when VS
Code changes its MCP UI.
