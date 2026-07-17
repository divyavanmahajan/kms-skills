#!/usr/bin/env python3
"""Regenerate wiki/dashboard.md — the health dashboard for the knowledge base.

Metrics (see policies/review-policy.md): page counts by status, sourced vs.
unsourced, stale pages, low-confidence pages, broken links, orphans.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import lint

ROOT = lint.ROOT
DASHBOARD = lint.WIKI / "dashboard.md"


def rel_link(page: Path) -> str:
    """Link target relative to the dashboard's directory (wiki/)."""
    return page.relative_to(lint.WIKI).as_posix()


def main():
    today = dt.date.today()
    pages = lint.wiki_pages()
    errors, warnings = lint.run(quiet=True)

    by_status: dict[str, int] = {}
    stale, unsourced, low_conf = [], [], []
    for page in pages:
        meta, err = lint.parse_frontmatter(page.read_text(encoding="utf-8"))
        if err or meta is None:
            continue
        status = str(meta.get("status", "unknown"))
        by_status[status] = by_status.get(status, 0) + 1
        if status == "superseded":
            continue
        review_after = lint.as_date(meta.get("review_after"))
        if review_after and review_after < today:
            stale.append((review_after, page, meta))
        if not meta.get("sources"):
            unsourced.append((page, meta))
        if meta.get("confidence") == "low":
            low_conf.append((page, meta))

    nuggets = lint.check_nuggets([], [])
    nugget_disputed = sum(1 for n in nuggets if n.get("status") == "disputed")

    active = [p for p in pages if p.name != "index.md"]
    stale.sort()
    broken = [e for e in errors if "broken link" in e]
    orphans = [w for w in warnings if "orphan page" in w]
    stale_pct = round(100 * len(stale) / len(active)) if active else 0

    lines = [
        "---",
        "title: Health Dashboard",
        "---",
        "",
        "# Health Dashboard",
        "",
        f"*Generated {today.isoformat()} by `scripts/dashboard.py` — do not edit by hand.*",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Pages | {len(pages)} |",
    ]
    for status in ("draft", "reviewed", "disputed", "superseded"):
        if status in by_status:
            lines.append(f"| — {status} | {by_status[status]} |")
    lines += [
        f"| Nuggets | {len(nuggets)} |",
        f"| — disputed | {nugget_disputed} |",
        f"| Stale (past review date) | {len(stale)} ({stale_pct}%) |",
        f"| Unsourced | {len(unsourced)} |",
        f"| Low confidence | {len(low_conf)} |",
        f"| Broken links | {len(broken)} |",
        f"| Orphan pages | {len(orphans)} |",
        f"| Lint errors / warnings | {len(errors)} / {len(warnings)} |",
        "",
    ]

    def section(title, rows):
        lines.append(f"## {title}")
        lines.append("")
        if rows:
            lines.extend(rows)
        else:
            lines.append("None. ✅")
        lines.append("")

    section("Pages needing review", [
        f"- [{m.get('title', p.stem)}]({rel_link(p)}) — due {d.isoformat()}"
        for d, p, m in stale
    ])
    section("Unsourced pages", [
        f"- [{m.get('title', p.stem)}]({rel_link(p)}) — status: {m.get('status')}"
        for p, m in unsourced
    ])
    section("Low-confidence pages", [
        f"- [{m.get('title', p.stem)}]({rel_link(p)})"
        for p, m in low_conf
    ])
    section("Structural issues", [f"- {e}" for e in broken + orphans])

    lines.append("*Next steps: run `/review` on stale pages; run `/contradictions` after large ingests.*")
    lines.append("")

    DASHBOARD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {DASHBOARD.relative_to(ROOT)} "
          f"({len(pages)} pages, {len(stale)} stale, {len(errors)} lint errors)")


if __name__ == "__main__":
    main()
