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


def _content_files() -> list[Path]:
    files = []
    for root in (NUGGETS_DIR, WIKI_DIR, SOURCES_DIR):
        if root.is_dir():
            files.extend(p for p in root.rglob("*") if p.is_file())
    if ENTITIES_FILE.is_file():
        files.append(ENTITIES_FILE)
    return sorted(files)


def content_hash() -> str:
    """Hash of everything the index is built from, for staleness detection.

    Byte-exact and machine-independent (stored in the manifest, compared in
    CI). Reads every content file — use content_fingerprint() for cheap
    repeated checks within a process.
    """
    h = hashlib.sha256()
    for path in _content_files():
        h.update(str(path.relative_to(REPO_ROOT)).encode())
        h.update(path.read_bytes())
    return h.hexdigest()


def content_fingerprint() -> str:
    """Cheap stat-based digest (path, size, mtime) of the content files.

    Changes whenever content_hash() would change (modulo mtime-only touches,
    which merely trigger one full re-hash). Used to memoize staleness checks
    so MCP tool calls don't re-read megabytes of sources on every invocation.
    """
    h = hashlib.sha256()
    for path in _content_files():
        stat = path.stat()
        h.update(f"{path.relative_to(REPO_ROOT)}:{stat.st_size}:{stat.st_mtime_ns};".encode())
    return h.hexdigest()
