# nugget-policy.md — Claim-Level Evidence Units

A **nugget** is a single, self-contained claim extracted from a source at
ingest time — richer than a chunk because it carries added context and
provenance instead of being an arbitrary text window. The design follows
Microsoft Web IQ's "structured evidence objects": passage-level units with
provenance, structural metadata, and enough local context to remain
interpretable when detached from the source (see
`wiki/topics/nuggets.md`).

Nuggets sit between `sources/` and `wiki/`: sources are evidence, nuggets are
the claim inventory, wiki pages are the synthesis. They make citation-drift
checks and contradiction sweeps mechanical — compare claims, not prose.

## What qualifies as a nugget

Extract a nugget for each claim that the citation policy says needs a source:
technical claims, comparisons, numbers/benchmarks/prices, version-specific
statements, notable direct quotes. Do NOT nuggetize navigation text, opinions
clearly framed as the source author's taste, or content already captured by an
existing nugget (update that nugget's context instead).

## Storage and schema

One YAML file per source: `nuggets/<same-slug-as-source>.yaml`.

```yaml
source: sources/web/2026-07-17-example.md   # must exist
created: 2026-07-17
nuggets:
  - id: example-p95-latency        # globally unique, kebab-case
    claim: >-                      # one atomic, self-contained statement.
      Web IQ serves grounding responses at sub-165 ms p95 latency.
    context: >-                    # what makes the claim interpretable alone:
      Vendor-reported figure from the June 2026 announcement, measured across
      five data centers; compared against unnamed competitors (~2.5x faster).
    quote: "sub-165ms p95 latency" # optional verbatim anchor from the source
    confidence: medium             # low | medium | high
    status: active                 # active | disputed | superseded
    superseded_by: other-nugget-id # required when status: superseded
    tags: [performance]
```

### The context rule (what makes it richer than a chunk)

The `context` field must resolve everything the bare claim leaves implicit:

- **Who says so** — vendor claim vs. independent measurement vs. opinion
- **When** — absolute dates, versions ("as of June 2026", "v2 only")
- **Scope** — conditions under which the claim holds
- **Resolved references** — no dangling "it/this/the system"; name things

A nugget whose claim + context can't be understood without opening the source
is a chunk with extra steps — rewrite it.

## Rules

1. Nugget claims are quotes-of-record: once created, a `claim` is not
   reworded. Corrections happen by superseding (new nugget, old one gets
   `status: superseded` + `superseded_by`). `context`, `confidence`,
   `status`, and `tags` may be updated (medium risk).
2. `confidence` is capped by the source `type`: `summary-notes` sources cap
   nuggets at `medium`.
3. Wiki pages should cite sources (as today) and MAY reference nugget ids in
   their *Sources* section for claim-level traceability.
4. Contradiction sweeps start from the nugget inventory; two nuggets about the
   same fact with incompatible claims both become `status: disputed` until
   resolved.
5. `scripts/lint.py` validates nugget files (schema, unique ids, source
   exists); the dashboard counts them.
