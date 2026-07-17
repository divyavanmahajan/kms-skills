#!/usr/bin/env python3
"""Sync Markdown notes from a public GitHub repo directory into inbox/.

Built for pulling episode summary notes (e.g. src/content/ainews in
divyavanmahajan.github.io — AI Daily Brief podcast summaries) into the KMS.
Listing uses the GitHub git-trees API; file content comes from
raw.githubusercontent.com. Both are unauthenticated (public repos only).

Config lives in feeds.yaml under `github_notes:`; dedup works like
fetch_feed.py — each written file carries a `guid:` (github:<repo>/<path>)
that is matched against inbox/ and sources/, so nothing is fetched twice.

Usage:
  python3 scripts/fetch_notes.py             # sync all configured note repos
  python3 scripts/fetch_notes.py --list      # dry run
  python3 scripts/fetch_notes.py --paths src/content/ainews/2026/07/foo.md \
      --source ainews                        # fetch specific files (no listing)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

import yaml

from fetch_feed import FEEDS_FILE, INBOX, ROOT, fetch, known_guids, slugify


def parse_note(raw: str):
    """Split an Astro-style note into (frontmatter dict, body)."""
    if raw.startswith("---\n"):
        end = raw.find("\n---", 4)
        if end != -1:
            try:
                meta = yaml.safe_load(raw[4:end]) or {}
            except yaml.YAMLError:
                meta = {}
            if isinstance(meta, dict):
                return meta, raw[end + 4:].lstrip("\n")
    return {}, raw


def list_tree(repo: str, branch: str) -> list[str]:
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    data = json.loads(fetch(url))
    if data.get("truncated"):
        print(f"[{repo}] WARNING: tree listing truncated", file=sys.stderr)
    return [t["path"] for t in data.get("tree", []) if t.get("type") == "blob"]


def iso_date(value) -> str:
    if isinstance(value, (dt.date, dt.datetime)):
        return (value.date() if isinstance(value, dt.datetime) else value).isoformat()
    if value:
        try:
            return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            pass
    return dt.date.today().isoformat()


def write_note(cfg: dict, path: str, raw: str) -> Path | None:
    meta, body = parse_note(raw)
    if meta.get("draft") is True:
        return None
    published = iso_date(meta.get("pubDate") or meta.get("date"))
    title = str(meta.get("title") or Path(path).stem)
    out = INBOX / f"note-{published}-{slugify(title)}.md"
    front = {
        "url": meta.get("url") or f"https://github.com/{cfg['repo']}/blob/{cfg.get('branch', 'main')}/{path}",
        "title": title,
        "author": cfg.get("author", f"summary notes from {cfg['repo']}"),
        "show": cfg.get("show"),
        "published": published,
        "retrieved": dt.date.today().isoformat(),
        "type": "summary-notes",
        "guid": f"github:{cfg['repo']}/{path}",
        "origin": f"github:{cfg['repo']}/{path}",
        "tags": meta.get("tags") or [],
        "description": meta.get("description"),
    }
    front = {k: v for k, v in front.items() if v is not None}
    out.write_text("---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True)
                   + "---\n\n" + body, encoding="utf-8")
    return out


def sync(cfg: dict, seen: set[str], dry: bool, only_paths: list[str] | None):
    name = cfg.get("name", cfg["repo"])
    repo, branch = cfg["repo"], cfg.get("branch", "main")
    prefix = cfg["path"].strip("/") + "/"
    if only_paths is not None:
        paths = only_paths
    else:
        paths = [p for p in list_tree(repo, branch)
                 if p.startswith(prefix) and p.endswith(".md")]
        paths.sort(reverse=True)  # YYYY/MM in the path => newest first
    limit = int(cfg.get("max_files", 20))
    new = [p for p in paths if f"github:{repo}/{p}" not in seen][:limit]
    for path in new:
        if dry:
            print(f"[{name}] NEW: {path}")
            continue
        raw = fetch(f"https://raw.githubusercontent.com/{repo}/{branch}/{path}").decode("utf-8")
        out = write_note(cfg, path, raw)
        if out is None:
            print(f"[{name}] skipped draft: {path}")
        else:
            seen.add(f"github:{repo}/{path}")
            print(f"[{name}] wrote {out.relative_to(ROOT)}")
    print(f"[{name}] {len(paths)} note files, {len(new)} new (limit {limit})")
    return len(new)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="dry run")
    ap.add_argument("--source", help="only sync the github_notes entry with this name")
    ap.add_argument("--paths", nargs="+",
                    help="specific repo file paths to fetch (skips tree listing)")
    args = ap.parse_args()

    config = yaml.safe_load(FEEDS_FILE.read_text(encoding="utf-8")) or {}
    sources = config.get("github_notes") or []
    if args.source:
        sources = [s for s in sources if s.get("name") == args.source]
        if not sources:
            sys.exit(f"no github_notes entry named '{args.source}' in feeds.yaml")
    if args.paths and len(sources) != 1:
        sys.exit("--paths requires exactly one source (use --source)")

    seen = known_guids()
    total = 0
    for cfg in sources:
        try:
            total += sync(cfg, seen, args.list, args.paths)
        except Exception as e:  # one bad repo shouldn't kill the run
            print(f"[{cfg.get('name', '?')}] ERROR: {e}", file=sys.stderr)
    print(f"done: {total} new note(s)" + (" (dry run)" if args.list else ""))


if __name__ == "__main__":
    main()
