#!/usr/bin/env python3
"""Extract named entities from nuggets into graph/entities.yaml (LLM-assisted).

The cache maps nugget uid ("<nugget file stem>#<claim id>") -> [{name, type}].
Only nuggets missing from the cache are processed, so this is cheap to run
after each ingest. The kms_mcp indexer turns the cache into Entity nodes and
MENTIONS edges in the knowledge graph.

Requires ANTHROPIC_API_KEY (or an `ant auth login` profile) and the
`anthropic` package.

Usage:
  python3 scripts/extract_entities.py            # extract for new nuggets
  python3 scripts/extract_entities.py --check    # list uncovered nuggets, exit 1 if any
  python3 scripts/extract_entities.py --model claude-haiku-4-5   # cheaper model
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
NUGGETS_DIR = ROOT / "nuggets"
ENTITIES_FILE = ROOT / "graph" / "entities.yaml"
BATCH_SIZE = 25

HEADER = """\
# Entity extraction cache — nugget uid ("<nugget file stem>#<claim id>") ->
# list of {name, type} named entities mentioned in the claim.
#
# Maintained by scripts/extract_entities.py (LLM-assisted). Like nuggets,
# entries are only ever added or corrected for NEW nuggets — the indexer
# (kms_mcp) turns this file into Entity nodes and MENTIONS edges.
"""

SYSTEM_PROMPT = """\
You extract named entities from knowledge-base claims for a knowledge graph.

Entity types (use exactly these strings): company, person, model (AI models/products),
organization (governments, universities, agencies, bands), report (named surveys/studies/
benchmarks/indexes/policy documents), technology (named tools/chips/protocols/techniques —
proper nouns only), place (countries/regions when geopolitically relevant), event.

Canonicalization rules (entities are shared graph nodes across the whole corpus):
- Use the most common short canonical name: "Nvidia" not "NVIDIA Corporation";
  "OpenAI", "Anthropic", "Google", "Meta", "Microsoft", "KPMG", "Menlo Ventures",
  "ChatGPT", "Claude", "Gemini", "United States", "China".
- Model families: keep versions distinct as written ("Claude 4", "o3", "Llama 4").
- People: "Firstname Lastname".
- Do NOT extract generic concepts ("AI agents", "enterprise adoption", "tariffs") —
  proper nouns only. 2-6 entities per claim is typical; an empty list is fine.

You will receive a list of claims, each with a uid. Return entities for every uid."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "uid": {"type": "string"},
                    "entities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {
                                    "type": "string",
                                    "enum": ["company", "person", "model",
                                             "organization", "report",
                                             "technology", "place", "event"],
                                },
                            },
                            "required": ["name", "type"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["uid", "entities"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
    "additionalProperties": False,
}


def load_all_nuggets() -> dict[str, dict]:
    nuggets: dict[str, dict] = {}
    for path in sorted(NUGGETS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for item in data.get("nuggets") or []:
            if isinstance(item, dict) and "id" in item:
                nuggets[f"{path.stem}#{item['id']}"] = item
    return nuggets


def load_cache() -> dict[str, list]:
    if not ENTITIES_FILE.is_file():
        return {}
    return yaml.safe_load(ENTITIES_FILE.read_text(encoding="utf-8")) or {}


def save_cache(cache: dict[str, list]) -> None:
    ENTITIES_FILE.parent.mkdir(exist_ok=True)
    with ENTITIES_FILE.open("w", encoding="utf-8") as out:
        out.write(HEADER)
        yaml.safe_dump({k: cache[k] for k in sorted(cache)}, out,
                       allow_unicode=True, sort_keys=False, width=100)


def extract_batch(client, model: str, batch: dict[str, dict]) -> dict[str, list]:
    import json

    lines = [f"uid: {uid}\nclaim: {n.get('claim', '')}\ncontext: {n.get('context', '')}"
             for uid, n in batch.items()]
    response = client.messages.create(
        model=model,
        max_tokens=16000,
        system=[{"type": "text", "text": SYSTEM_PROMPT,
                 "cache_control": {"type": "ephemeral"}}],
        output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        messages=[{"role": "user", "content": "\n\n".join(lines)}],
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("Model refused the extraction request")
    text = next(b.text for b in response.content if b.type == "text")
    return {r["uid"]: r["entities"] for r in json.loads(text)["results"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="only report nuggets missing from the cache")
    parser.add_argument("--model", default="claude-opus-4-8")
    args = parser.parse_args()

    nuggets = load_all_nuggets()
    cache = load_cache()
    missing = {uid: n for uid, n in nuggets.items() if uid not in cache}

    if args.check:
        for uid in sorted(missing):
            print(uid)
        print(f"{len(missing)} of {len(nuggets)} nuggets lack entity extraction",
              file=sys.stderr)
        return 1 if missing else 0

    if not missing:
        print("Entity cache is complete — nothing to extract.")
        return 0

    import anthropic
    client = anthropic.Anthropic()

    uids = sorted(missing)
    for start in range(0, len(uids), BATCH_SIZE):
        batch = {uid: missing[uid] for uid in uids[start:start + BATCH_SIZE]}
        print(f"Extracting {start + 1}-{start + len(batch)} of {len(uids)}...")
        cache.update(extract_batch(client, args.model, batch))
        save_cache(cache)  # checkpoint after each batch

    print(f"Done: {len(uids)} nuggets extracted -> {ENTITIES_FILE.relative_to(ROOT)}")
    print("Rebuild the graph with: python3 -m kms_mcp index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
