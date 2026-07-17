#!/usr/bin/env python3
"""Scaffold a schema-compliant wiki page (see policies/schema.md).

Usage:
  python3 scripts/new_page.py "LLM Wiki" --type topic
  python3 scripts/new_page.py "Use MkDocs for the site" --type decision
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

TOPIC_BODY = """## Summary

TODO — 2–5 sentences.

## Open questions

- TODO

## Sources

- TODO
"""

DECISION_BODY = """## Context

TODO

## Decision

TODO

## Consequences

TODO
"""


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("title")
    ap.add_argument("--type", choices=["topic", "decision"], default="topic")
    ap.add_argument("--interval", type=int, default=None,
                    help="review_interval_days (default: 90 topic, none for decision)")
    args = ap.parse_args()

    today = dt.date.today()
    slug = slugify(args.title)

    if args.type == "decision":
        folder = WIKI / "decisions"
        existing = sorted(folder.glob("[0-9][0-9][0-9][0-9]-*.md"))
        seq = int(existing[-1].name[:4]) + 1 if existing else 1
        path = folder / f"{seq:04d}-{slug}.md"
        body = DECISION_BODY
        interval_line = ""
        review_after = today + dt.timedelta(days=365 * 5)  # decisions: review when superseded
    else:
        path = WIKI / "topics" / f"{slug}.md"
        body = TOPIC_BODY
        interval = args.interval or 90
        interval_line = f"review_interval_days: {interval}\n"
        review_after = today + dt.timedelta(days=interval)

    if path.exists():
        raise SystemExit(f"refusing to overwrite existing page: {path.relative_to(ROOT)}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f"title: {args.title}\n"
        "status: draft\n"
        "confidence: low\n"
        f"created: {today.isoformat()}\n"
        f"review_after: {review_after.isoformat()}\n"
        f"{interval_line}"
        "sources: []\n"
        "tags: []\n"
        "---\n\n"
        f"# {args.title}\n\n{body}",
        encoding="utf-8",
    )
    print(f"created {path.relative_to(ROOT)}")
    print("remember: link it from at least one existing page (orphan check), "
          "add sources, then run scripts/lint.py")


if __name__ == "__main__":
    main()
