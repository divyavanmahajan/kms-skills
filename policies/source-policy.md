# source-policy.md — Raw Material Preservation

Generated pages sit *above* sources, never in place of them. Compiled summaries
can be regenerated; lost sources cannot.

## Layout

```
sources/
  web/    YYYY-MM-DD-slug.md     — snapshots/notes of web articles
  docs/   YYYY-MM-DD-slug.(pdf|md) — papers, PDFs, formal docs (+ .md notes alongside)
  notes/  YYYY-MM-DD-slug.md     — the owner's own notes, meeting notes, drafts
  code/   YYYY-MM-DD-slug.md     — extracts from codebases, READMEs, ADRs, API docs
```

## Rules

1. **Append-only.** Existing source files are never edited or deleted. A newer
   version of the same source gets a new dated file.
2. **Record retrieval metadata.** Every source file starts with a frontmatter
   block:

   ```yaml
   ---
   url: https://...            # or origin: <repo/path/person> for non-web sources
   retrieved: 2026-07-17
   type: snapshot | summary-notes | original | extract
   ---
   ```

   `type: summary-notes` marks files that are notes *about* a source rather than
   a verbatim copy — pages citing them inherit at most `confidence: medium`.
3. **Binary sources get a sidecar.** A PDF `foo.pdf` gets `foo.md` next to it
   with the frontmatter above plus extracted key passages.
4. **Sources are not wiki pages.** They are exempt from `schema.md` and are not
   published to the site. Never "clean up" a source to match current terminology
   — that destroys the evidence trail.
5. **Inbox flow.** New material lands in `inbox/`, the `/ingest` skill moves it
   to the right `sources/` subfolder with a dated name, then compiles it.
