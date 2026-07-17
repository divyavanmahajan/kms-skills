---
url: https://arxiv.org/abs/2411.09607
title: Initial Nugget Evaluation Results for the TREC 2024 RAG Track with the AutoNuggetizer Framework
author: Ronak Pradeep, Nandan Thakur, Shivani Upadhyay, Daniel Campos, Nick Craswell, Jimmy Lin (U. Waterloo / Snowflake / Microsoft)
published: 2024-11-14
retrieved: 2026-07-17
type: summary-notes
---

# AutoNuggetizer / TREC 2024 RAG Track — summary notes

## What it is

The AutoNuggetizer framework modernizes ("refactors") the nugget evaluation
methodology — originally developed by Voorhees for the 2003 TREC Question
Answering Track's definition questions — using LLMs to automate both nugget
creation and nugget assignment, for evaluating RAG systems in the TREC 2024
RAG Track.

## Nugget creation

- Automatic (AutoNuggets): GPT-4o processes documents judged relevant
  (grade ≥1), iteratively refines nugget lists, generates up to 30 candidates
  per query, outputs 20 ranked nuggets by importance.
- Semi-manual (AutoNuggets+Edits): NIST assessors post-edit the automatic
  nuggets (add/eliminate/combine), ~1 hour per topic.
- Nuggets are classified **vital** ("must appear in a good response") vs.
  **okay** (valuable but non-essential context).

## Nugget assignment

- Automatic (AutoAssign): GPT-4o, listwise, ≤10 nuggets per call; each nugget
  judged "support" / "partial_support" / "not_support" against an answer.
- Manual (ManualAssign): NIST assessor, same three categories.

## Scoring

Six variants; run score = mean over queries. Primary metric V_strict: average
strict matching over vital nuggets only (1 for full support, else 0). Variants
credit partial support at 0.5 and/or weight okay nuggets at 0.5 (V, A_strict,
A, W_strict, W).

## Track setup

TREC 2024 RAG Track tasks: Retrieval (MS MARCO V2.1 deduped, 113.5M
passages), Augmented Generation (top-100 provided), full RAG. 301 non-factoid
topics from Bing search logs.

## Key findings

- Strong run-level correlation between fully automatic and (mostly) manual
  nugget evaluation: Kendall's τ = 0.783 at run level; much lower per
  topic/run (τ = 0.324) — system rankings stable, granular agreement noisy.
- 93 RAG + 53 AG submissions; 31 RAG / 14 AG runs evaluated by NIST. Top
  V_strict ≈ 0.67 (manual) / 0.48 (automatic).
- AG runs comparable to full RAG (provided reference lists were effective).
- Longer answers loosely correlate with higher V_strict, with wide variance.
- Explicitly excluded: answer support / citation appropriateness (i.e.,
  hallucination assessment is out of scope for this report).
