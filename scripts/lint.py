#!/usr/bin/env python3
"""Structural lint for the wiki (see policies/schema.md).

Checks maintainability, not truth:
  - frontmatter present, valid YAML, required keys, legal values
  - superseded pages point to an existing replacement
  - listed sources exist on disk
  - internal Markdown links resolve
  - orphan pages (nothing links to them)
  - kebab-case file names

Errors exit 1. Warnings exit 0 unless --strict.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
GENERATED = {"dashboard.md"}  # exempt from schema; never orphans, links from it don't count
REQUIRED_KEYS = ("title", "status", "confidence", "review_after", "sources")
STATUSES = {"draft", "reviewed", "disputed", "superseded"}
CONFIDENCES = {"low", "medium", "high"}
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$|^\d{4}-[a-z0-9-]+\.md$")


def parse_frontmatter(text: str):
    """Return (dict-or-None, error-or-None)."""
    if not text.startswith("---\n"):
        return None, "missing frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "unterminated frontmatter"
    try:
        meta = yaml.safe_load(text[4:end])
    except yaml.YAMLError as e:
        return None, f"invalid YAML frontmatter: {e}"
    if not isinstance(meta, dict):
        return None, "frontmatter is not a mapping"
    return meta, None


def wiki_pages():
    return sorted(p for p in WIKI.rglob("*.md") if p.name not in GENERATED)


def as_date(value):
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def check_frontmatter(page: Path, meta: dict, errors, warnings):
    rel = page.relative_to(ROOT)
    for key in REQUIRED_KEYS:
        if key not in meta:
            errors.append(f"{rel}: missing required frontmatter key '{key}'")
    status = meta.get("status")
    if status is not None and status not in STATUSES:
        errors.append(f"{rel}: invalid status '{status}' (want {'|'.join(sorted(STATUSES))})")
    conf = meta.get("confidence")
    if conf is not None and conf not in CONFIDENCES:
        errors.append(f"{rel}: invalid confidence '{conf}'")
    if "review_after" in meta and as_date(meta["review_after"]) is None:
        errors.append(f"{rel}: review_after is not a YYYY-MM-DD date")

    sources = meta.get("sources")
    if sources is not None:
        if not isinstance(sources, list):
            errors.append(f"{rel}: 'sources' must be a list")
            sources = []
        for src in sources:
            if not (ROOT / str(src)).exists():
                errors.append(f"{rel}: listed source does not exist: {src}")
        # citation-policy: navigation pages (index) may be unsourced
        if not sources and status not in (None, "draft") and page.name != "index.md":
            warnings.append(f"{rel}: no sources listed but status is '{status}' "
                            "(citation-policy: only drafts may be unsourced)")

    if status == "superseded":
        target = meta.get("superseded_by")
        if not target:
            errors.append(f"{rel}: superseded page missing 'superseded_by'")
        elif not (WIKI / str(target)).exists():
            errors.append(f"{rel}: superseded_by target does not exist: {target}")


def check_links(page: Path, body: str, errors):
    rel = page.relative_to(ROOT)
    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (page.parent / path_part).resolve()
        if not resolved.exists():
            errors.append(f"{rel}: broken link -> {target}")


def collect_internal_targets(page: Path, body: str):
    targets = set()
    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path_part = target.split("#", 1)[0]
        if path_part:
            targets.add((page.parent / path_part).resolve())
    return targets


def run(strict: bool = False, quiet: bool = False):
    errors, warnings = [], []
    pages = wiki_pages()
    linked = set()

    for page in pages:
        rel = page.relative_to(ROOT)
        text = page.read_text(encoding="utf-8")
        if not KEBAB_RE.match(page.name):
            warnings.append(f"{rel}: file name is not kebab-case")
        meta, err = parse_frontmatter(text)
        if err:
            errors.append(f"{rel}: {err}")
        else:
            check_frontmatter(page, meta, errors, warnings)
        check_links(page, text, errors)
        linked |= collect_internal_targets(page, text)

    # Orphans: wiki pages (except the home page) that no wiki page links to.
    for page in pages:
        if page.name == "index.md":
            continue
        if page.resolve() not in linked:
            warnings.append(f"{page.relative_to(ROOT)}: orphan page (no wiki page links to it)")

    if not quiet:
        for e in errors:
            print(f"ERROR   {e}")
        for w in warnings:
            print(f"WARNING {w}")
        print(f"\nlint: {len(pages)} pages, {len(errors)} errors, {len(warnings)} warnings")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()
    errors, warnings = run(strict=args.strict)
    if errors or (args.strict and warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
