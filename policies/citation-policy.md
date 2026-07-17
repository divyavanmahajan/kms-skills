# citation-policy.md — What Requires a Source

The compiled layer is only trustworthy if claims trace back to raw material.
"A summary you already compiled has to be actively kept honest."

## Always require a source

- Technical claims (how a tool/API/system behaves)
- Comparisons between tools, methods, or products
- Version-specific statements ("since v2, ...")
- Numbers: benchmarks, prices, limits, dates
- Anything security-related

Pages making such claims must list the supporting file in frontmatter `sources:`
AND name it in the `## Sources` section with a one-line note on what it supports.

## May be unsourced

- Definitions the page itself establishes (glossary entries derived from usage)
- The author's own decisions and preferences (recorded in `wiki/decisions/`)
- Structural/navigation text

## Handling unsourced claims

If a claim can't be sourced: move it to *Open questions*, set
`confidence: low`, and keep `status: draft` (or mark `disputed` if it conflicts
with a sourced claim). Never delete the claim silently — that hides the drift.

## Citation drift

After any rewrite of a page, re-check that each remaining claim is still
supported by the sources listed — a citation that no longer matches its claim is
worse than no citation ("false confidence"). The `/review` skill performs this
check; it must run before a `draft → reviewed` transition.
