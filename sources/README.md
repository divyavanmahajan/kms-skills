# sources/ — raw material (append-only)

Rules live in [`policies/source-policy.md`](../policies/source-policy.md).
Short version: files here are never edited or deleted; new versions of a source
get a new dated file; every file starts with `url:`/`origin:`, `retrieved:`,
and `type:` frontmatter.

- `web/` — snapshots/notes of web articles
- `docs/` — papers, PDFs, formal documents (binaries get a `.md` sidecar)
- `notes/` — the owner's own notes and drafts
- `code/` — extracts from codebases, READMEs, ADRs, API docs
- `audio/` — transcripts of recordings and podcast episodes (audio binaries
  are not committed; see `policies/source-policy.md`)
