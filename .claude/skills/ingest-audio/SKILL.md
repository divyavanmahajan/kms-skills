---
name: ingest-audio
description: Ingest an audio recording or podcast episode — collect required metadata (asking the user for anything missing), obtain a transcript, preserve it under sources/audio/, extract nuggets, and compile wiki pages. Use for audio files, voice memos, meeting recordings, podcast episodes, or feed-entry files in inbox/ produced by scripts/fetch_feed.py.
---

# Ingest audio / podcast episodes

Follow `AGENTS.md`, `policies/source-policy.md`, and `policies/nugget-policy.md`.
This extends the `ingest` skill for audio: the extra work is metadata
collection and transcription; everything downstream is the normal pipeline.

## Input

`$ARGUMENTS` may be: an audio file path, a transcript file, a feed-entry file
in `inbox/` (from `scripts/fetch_feed.py`), or an episode URL. If empty,
process every `inbox/podcast-*.md` feed entry.

## Step 1 — Collect metadata (ask, don't guess)

Required metadata for every audio source:

| Field | Notes |
|---|---|
| `title` | Episode or recording title |
| `published` / recorded date | Absolute date (YYYY-MM-DD) |
| `speakers` | List with roles, e.g. "Jane Doe (host)", "R. Roe (guest, VP Eng at Acme)" |
| `url` or `origin` | Episode page URL, or `origin: personal recording — <occasion>` |
| `show` | Series/show name (omit for one-off recordings) |
| `type` | `transcript` (verbatim) or `feed-entry` (show notes only) |

Feed entries arrive with most of this filled; personal recordings usually
arrive with none of it. **For every required field you cannot determine from
the file, the feed, or the episode page: ASK THE USER** — use the
AskUserQuestion tool when available (batch all missing fields into one round),
otherwise ask in plain text and wait. Do not invent speaker names or dates; do
not proceed with placeholders. Optional but worth asking when relevant:
language (default `en`) and whether a personal recording is sensitive/private
(if yes, note `sensitivity: private` so it's flagged before the repo is ever
made public).

## Step 2 — Obtain a transcript

In order of preference:

1. A transcript file supplied alongside the audio, or one linked from the feed
   (`<podcast:transcript>` tag or the episode page).
2. Local transcription if tooling exists: check `command -v whisper`,
   `whisper-cpp`, or `ffmpeg` + an available transcription tool.
3. Neither available → ASK THE USER: install openai-whisper (`pip install
   openai-whisper`, large download; needs ffmpeg), paste/attach a transcript,
   or ingest show-notes-only for now.

If only show notes are available, proceed with `type: feed-entry` and record
"transcript pending" in the source file — a later run can supersede with the
full transcript as a NEW dated source file (sources are append-only).

## Step 3 — Preserve

Write `sources/audio/YYYY-MM-DD-<show-or-slug>-<episode-slug>.md` (date =
published/recorded date) with the full metadata block from Step 1 plus
`retrieved:` and `guid:` (from the feed entry, if any), then the transcript
(speaker-labelled where possible) or show notes. `git mv` processed feed
entries out of `inbox/`. **Do not commit the audio binary** — record
`audio_url:` (or the local path) instead; if the user explicitly wants the
audio archived, put it in `sources/audio/media/` with the source file as its
sidecar.

## Step 4 — Nuggets and compilation

Run the `nuggets` skill's procedure on the new source. Audio-specific rules:

- Spoken claims are testimony: `context` MUST name the speaker and their role
  ("claim by guest X, CTO of Y, on <show> episode of <date>"). Confidence caps
  at `medium` for verbatim transcripts, `low` for show-notes-only sources.
- Distinguish the host's framing from the guest's claims.
- Then compile per the `ingest` skill Step 3: **update existing topic pages** —
  never create a page per episode (structure drift). A per-show hub page
  listing ingested episodes is the most that's warranted, and only once a show
  has several episodes.
- Pages leaning on podcast claims should get `review_interval_days: 30–90`.

## Step 5 — Verify, commit, report

`python3 scripts/lint.py`, `python3 scripts/dashboard.py`, commit as
`ingest: <show/recording> <episode/date>` (medium risk — branch/PR unless told
otherwise). Report: metadata gathered (and what you had to ask for), transcript
status, nugget count, pages touched, contradictions raised.
