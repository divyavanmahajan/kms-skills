"""Repo-relative paths and constants for the KMS MCP server."""

import hashlib
import os
from pathlib import Path


def find_repo_root() -> Path:
    """Locate the knowledge repo root.

    Honours $KMS_REPO_ROOT, otherwise walks up from this package looking for
    the directory that contains both nuggets/ and wiki/.
    """
    env = os.environ.get("KMS_REPO_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve().parent
    for candidate in (here, *here.parents):
        if (candidate / "nuggets").is_dir() and (candidate / "wiki").is_dir():
            return candidate
    raise RuntimeError(
        "Could not locate the KMS repo root (no nuggets/ + wiki/ found). "
        "Set KMS_REPO_ROOT to the repository path."
    )


REPO_ROOT = find_repo_root()
NUGGETS_DIR = REPO_ROOT / "nuggets"
WIKI_DIR = REPO_ROOT / "wiki"
SOURCES_DIR = REPO_ROOT / "sources"
ENTITIES_FILE = REPO_ROOT / "graph" / "entities.yaml"

INDEX_DIR = REPO_ROOT / ".kms-index"
DB_FILE = INDEX_DIR / "kms.kuzu"
MANIFEST_FILE = INDEX_DIR / "manifest.json"
MODEL_CACHE_DIR = INDEX_DIR / "models"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


def content_hash() -> str:
    """Hash of everything the index is built from, for staleness detection."""
    h = hashlib.sha256()
    roots = [NUGGETS_DIR, WIKI_DIR, SOURCES_DIR]
    files = []
    for root in roots:
        if root.is_dir():
            files.extend(p for p in root.rglob("*") if p.is_file())
    if ENTITIES_FILE.is_file():
        files.append(ENTITIES_FILE)
    for path in sorted(files):
        h.update(str(path.relative_to(REPO_ROOT)).encode())
        h.update(path.read_bytes())
    return h.hexdigest()
