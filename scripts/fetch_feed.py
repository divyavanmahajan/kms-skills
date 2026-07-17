#!/usr/bin/env python3
"""Fetch podcast RSS/Atom feeds (including private Patreon feeds) into inbox/.

Reads feeds.yaml at the repo root, fetches each feed, and writes one Markdown
file per NEW episode into inbox/ (frontmatter + show notes). Episodes already
present in inbox/ or sources/audio/ (matched by guid) are skipped, so state
lives in the files themselves — no separate state file.

Feed URLs may reference environment variables as ${VAR_NAME} so private feed
URLs (e.g. Patreon's per-user RSS link, which embeds an auth token) never get
committed.

Usage:
  python3 scripts/fetch_feed.py            # fetch all feeds, write new entries
  python3 scripts/fetch_feed.py --list     # dry run: show what would be written
  python3 scripts/fetch_feed.py --feed nameA  # only the named feed
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FEEDS_FILE = ROOT / "feeds.yaml"
INBOX = ROOT / "inbox"
AUDIO_SOURCES = ROOT / "sources" / "audio"
GUID_RE = re.compile(r"^guid:\s*(.+?)\s*$", re.M)
ATOM = "{http://www.w3.org/2005/Atom}"


def expand_env(url: str) -> str:
    def sub(m):
        val = os.environ.get(m.group(1))
        if val is None:
            raise KeyError(f"environment variable {m.group(1)} is not set "
                           f"(required by a feed URL in feeds.yaml)")
        return val
    return re.sub(r"\$\{([A-Za-z0-9_]+)\}", sub, url)


def slugify(text: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-") or "untitled"


def strip_html(text: str) -> str:
    text = re.sub(r"<br\s*/?>|</p>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def known_guids() -> set[str]:
    guids = set()
    for folder in (INBOX, AUDIO_SOURCES):
        if not folder.exists():
            continue
        for f in folder.glob("*.md"):
            guids |= set(GUID_RE.findall(f.read_text(encoding="utf-8")))
    return guids


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "kms-skills feed fetcher"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def parse_date(value: str | None):
    if not value:
        return None
    for parser in (parsedate_to_datetime, dt.datetime.fromisoformat):
        try:
            return parser(value.strip())
        except (ValueError, TypeError):
            continue
    return None


def parse_entries(raw: bytes) -> list[dict]:
    root = ET.fromstring(raw)
    entries = []
    if root.tag == f"{ATOM}feed":  # Atom
        show = (root.findtext(f"{ATOM}title") or "").strip()
        for e in root.findall(f"{ATOM}entry"):
            link = ""
            audio_url = ""
            for l in e.findall(f"{ATOM}link"):
                rel = l.get("rel", "alternate")
                if rel == "enclosure":
                    audio_url = l.get("href", "")
                elif rel == "alternate":
                    link = l.get("href", "")
            entries.append({
                "show": show,
                "title": (e.findtext(f"{ATOM}title") or "").strip(),
                "guid": (e.findtext(f"{ATOM}id") or link).strip(),
                "link": link,
                "audio_url": audio_url,
                "published": parse_date(e.findtext(f"{ATOM}published")
                                        or e.findtext(f"{ATOM}updated")),
                "notes": strip_html(e.findtext(f"{ATOM}content")
                                    or e.findtext(f"{ATOM}summary") or ""),
            })
    else:  # RSS 2.0
        channel = root.find("channel")
        if channel is None:
            raise ValueError("unrecognized feed format (neither Atom nor RSS 2.0)")
        show = (channel.findtext("title") or "").strip()
        for item in channel.findall("item"):
            enclosure = item.find("enclosure")
            link = (item.findtext("link") or "").strip()
            entries.append({
                "show": show,
                "title": (item.findtext("title") or "").strip(),
                "guid": (item.findtext("guid") or link).strip(),
                "link": link,
                "audio_url": enclosure.get("url", "") if enclosure is not None else "",
                "published": parse_date(item.findtext("pubDate")),
                "notes": strip_html(item.findtext("description") or ""),
            })
    return entries


def write_entry(feed_name: str, entry: dict) -> Path:
    published = entry["published"]
    date_str = published.date().isoformat() if published else dt.date.today().isoformat()
    path = INBOX / f"podcast-{date_str}-{slugify(entry['title'])}.md"
    meta = {
        "url": entry["link"] or entry["audio_url"],
        "retrieved": dt.date.today().isoformat(),
        "type": "feed-entry",
        "feed": feed_name,
        "show": entry["show"],
        "episode": entry["title"],
        "published": date_str,
        "guid": entry["guid"],
        "audio_url": entry["audio_url"],
        "transcript": None,  # filled during /ingest-audio
    }
    body = (f"# {entry['show']} — {entry['title']}\n\n"
            f"## Show notes (from feed)\n\n{entry['notes'] or '(none provided)'}\n")
    path.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True)
                    + "---\n\n" + body, encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="dry run, print new entries only")
    ap.add_argument("--feed", help="only fetch the feed with this name")
    args = ap.parse_args()

    if not FEEDS_FILE.exists():
        sys.exit("feeds.yaml not found — copy the template at the repo root and add feeds")
    config = yaml.safe_load(FEEDS_FILE.read_text(encoding="utf-8")) or {}
    feeds = config.get("feeds") or []
    if args.feed:
        feeds = [f for f in feeds if f.get("name") == args.feed]
        if not feeds:
            sys.exit(f"no feed named '{args.feed}' in feeds.yaml")

    seen = known_guids()
    total_new = 0
    for feed in feeds:
        name = feed.get("name", "unnamed")
        try:
            url = expand_env(str(feed["url"]))
            raw = fetch(url)
            entries = parse_entries(raw)
        except Exception as e:  # keep one bad feed from killing the run
            print(f"[{name}] ERROR: {e}", file=sys.stderr)
            continue
        # Only look at the newest N feed entries, THEN drop known guids —
        # otherwise each run would backfill ever-older archive episodes.
        limit = int(feed.get("max_episodes", 5))
        recent = sorted(entries,
                        key=lambda e: e["published"].timestamp() if e["published"] else 0.0,
                        reverse=True)[:limit]
        new = [e for e in recent if e["guid"] and e["guid"] not in seen]
        for entry in new:
            if args.list:
                print(f"[{name}] NEW: {entry['title']} ({entry['guid']})")
            else:
                path = write_entry(name, entry)
                seen.add(entry["guid"])
                print(f"[{name}] wrote {path.relative_to(ROOT)}")
        total_new += len(new)
        print(f"[{name}] {len(entries)} entries in feed, {len(new)} new")
    print(f"done: {total_new} new episode(s)" + (" (dry run)" if args.list else ""))


if __name__ == "__main__":
    main()
