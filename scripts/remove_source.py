#!/usr/bin/env python3
"""Remove (retract) source files and the mechanically-derived content.

Given a glob pattern matching files under sources/, this script computes the
full downstream impact and — with --apply — performs the *mechanical* part of
a retraction:

  - deletes the matched source files
  - deletes the nugget files whose `source:` points at them
  - prunes their nuggets' entries from graph/entities.yaml
  - removes the source paths from wiki frontmatter `sources:` lists and from
    `## Sources` bullet lines
  - appends the removal (path + guid) to sources/RETRACTIONS.md, an append-only
    log that also acts as a guid tombstone so fetch_feed.py / fetch_notes.py
    never re-ingest a retracted source

What it deliberately does NOT do: rewrite wiki prose. Claims in page bodies
that rest solely on a removed source are judgment work — the remove-source
skill (an LLM pass) handles those, guided by this script's report.

Usage:
  python3 scripts/remove_source.py "audio/2025-04-*"            # dry-run impact report
  python3 scripts/remove_source.py "sources/web/*foo*" --apply --reason "duplicate ingest"
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
NUGGETS = ROOT / "nuggets"
WIKI = ROOT / "wiki"
ENTITIES_FILE = ROOT / "graph" / "entities.yaml"
RETRACTIONS = SOURCES / "RETRACTIONS.md"

RETRACTIONS_HEADER = """\
# Retraction log

Append-only record of sources removed from the KMS (the one sanctioned way
content leaves `sources/`). Each entry keeps the source's `guid:` at column 0
so `fetch_feed.py` / `fetch_notes.py` treat retracted sources as already known
and never re-ingest them. Never edit or delete entries. Full content remains
recoverable from git history.
"""

GUID_RE = re.compile(r"^guid:\s*(.+?)\s*$", re.M)
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def resolve_pattern(pattern: str) -> list[Path]:
    """Glob under the repo root, trying the pattern as given and under sources/."""
    matches = {p for p in ROOT.glob(pattern) if p.is_file()}
    if not pattern.startswith("sources/"):
        matches |= {p for p in ROOT.glob(f"sources/{pattern}") if p.is_file()}
    matched = sorted(p for p in matches
                     if p.is_relative_to(SOURCES) and p.name != RETRACTIONS.name)
    return matched


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def compute_impact(source_paths: list[Path]) -> dict:
    source_rels = {rel(p) for p in source_paths}

    guids: dict[str, str] = {}
    for p in source_paths:
        m = GUID_RE.search(p.read_text(encoding="utf-8"))
        if m:
            guids[rel(p)] = m.group(1).strip("'\"")

    nugget_files: list[Path] = []
    nugget_uids: list[str] = []
    for nf in sorted(NUGGETS.glob("*.yaml")):
        data = yaml.safe_load(nf.read_text(encoding="utf-8")) or {}
        if str(data.get("source", "")) in source_rels:
            nugget_files.append(nf)
            nugget_uids.extend(f"{nf.stem}#{n['id']}"
                               for n in data.get("nuggets") or []
                               if isinstance(n, dict) and "id" in n)

    entity_keys: list[str] = []
    if ENTITIES_FILE.is_file():
        cache = yaml.safe_load(ENTITIES_FILE.read_text(encoding="utf-8")) or {}
        entity_keys = sorted(set(cache) & set(nugget_uids))

    pages: dict[str, dict] = {}
    for page in sorted(WIKI.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        hit = sorted(s for s in source_rels if s in text)
        if not hit:
            continue
        meta = {}
        m = FRONTMATTER_RE.match(text)
        if m:
            try:
                meta = yaml.safe_load(m.group(1)) or {}
            except yaml.YAMLError:
                meta = {}
        fm_sources = [str(s) for s in meta.get("sources") or []]
        remaining = [s for s in fm_sources if s not in source_rels]
        pages[rel(page)] = {
            "referenced_sources": hit,
            "loses_all_sources": bool(fm_sources) and not remaining,
            "remaining_sources": len(remaining),
        }

    return {
        "sources": sorted(source_rels),
        "guids": guids,
        "nugget_files": [rel(p) for p in nugget_files],
        "nugget_uids": sorted(nugget_uids),
        "entity_keys": entity_keys,
        "pages": pages,
    }


def print_report(impact: dict) -> None:
    print(f"Sources matched ({len(impact['sources'])}):")
    for s in impact["sources"]:
        guid = impact["guids"].get(s)
        print(f"  {s}" + (f"  [guid: {guid}]" if guid else ""))
    print(f"\nNugget files to delete ({len(impact['nugget_files'])}), "
          f"{len(impact['nugget_uids'])} nuggets:")
    for n in impact["nugget_files"]:
        print(f"  {n}")
    print(f"\nEntity cache entries to prune: {len(impact['entity_keys'])}")
    print(f"\nWiki pages referencing these sources ({len(impact['pages'])}):")
    for path, info in impact["pages"].items():
        note = ("LOSES ALL SOURCES — needs removal/supersede decision"
                if info["loses_all_sources"]
                else f"{info['remaining_sources']} source(s) remain — "
                     f"claims from the removed source(s) need manual review")
        print(f"  {path}  ({note})")
    if not impact["pages"]:
        print("  (none)")


def prune_page_citations(page: Path, source_rels: set[str]) -> None:
    """Drop frontmatter `sources:` entries and `## Sources` bullets that
    reference removed paths. Line-based to preserve formatting; body prose is
    left for the LLM pass."""
    lines = page.read_text(encoding="utf-8").splitlines(keepends=True)
    out = []
    for line in lines:
        stripped = line.strip()
        references = any(s in line for s in source_rels)
        is_list_item = stripped.startswith("- ") or stripped.startswith("-\t")
        if references and is_list_item:
            continue
        out.append(line)
    page.write_text("".join(out), encoding="utf-8")


def apply(impact: dict, reason: str) -> None:
    source_rels = set(impact["sources"])

    entry_lines = [f"\n## {dt.date.today().isoformat()} — {reason}\n"]
    for s in impact["sources"]:
        entry_lines.append(f"path: {s}\n")
        if s in impact["guids"]:
            entry_lines.append(f"guid: {impact['guids'][s]}\n")
    if not RETRACTIONS.is_file():
        RETRACTIONS.write_text(RETRACTIONS_HEADER, encoding="utf-8")
    with RETRACTIONS.open("a", encoding="utf-8") as log:
        log.writelines(entry_lines)

    for s in impact["sources"]:
        (ROOT / s).unlink()
    for n in impact["nugget_files"]:
        (ROOT / n).unlink()

    if impact["entity_keys"] and ENTITIES_FILE.is_file():
        text = ENTITIES_FILE.read_text(encoding="utf-8")
        header = "".join(line for line in text.splitlines(keepends=True)
                         if line.startswith("#"))
        cache = yaml.safe_load(text) or {}
        for key in impact["entity_keys"]:
            cache.pop(key, None)
        with ENTITIES_FILE.open("w", encoding="utf-8") as out:
            out.write(header)
            yaml.safe_dump({k: cache[k] for k in sorted(cache)}, out,
                           allow_unicode=True, sort_keys=False, width=100)

    for path in impact["pages"]:
        prune_page_citations(ROOT / path, source_rels)

    print(f"Applied: removed {len(impact['sources'])} sources, "
          f"{len(impact['nugget_files'])} nugget files, "
          f"{len(impact['entity_keys'])} entity entries; "
          f"pruned citations in {len(impact['pages'])} pages; "
          f"logged to {rel(RETRACTIONS)}.")
    print("Still manual: page-body claims derived from the removed sources, "
          "and pages that lost all sources. Then: lint, dashboard, reindex.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pattern",
                        help='glob under sources/, e.g. "audio/2025-04-*" or "sources/web/*foo*"')
    parser.add_argument("--apply", action="store_true",
                        help="perform the mechanical removals (default: dry-run report)")
    parser.add_argument("--reason", default="owner-requested removal",
                        help="recorded in sources/RETRACTIONS.md")
    args = parser.parse_args()

    matched = resolve_pattern(args.pattern)
    if not matched:
        print(f"No files under sources/ match {args.pattern!r}", file=sys.stderr)
        return 1

    impact = compute_impact(matched)
    print_report(impact)
    if args.apply:
        print()
        apply(impact, args.reason)
    else:
        print("\nDry run — re-run with --apply to perform the mechanical removals.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
