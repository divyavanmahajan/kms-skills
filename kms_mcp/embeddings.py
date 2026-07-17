"""Local sentence embeddings (all-MiniLM-L6-v2 via fastembed's ONNX runtime).

The model (~90MB) is downloaded once into .kms-index/models and reused
offline afterwards. Vectors are L2-normalised so cosine similarity is a
plain dot product.
"""

import numpy as np

from .config import EMBEDDING_MODEL, MODEL_CACHE_DIR

_model = None


def get_model():
    global _model
    if _model is None:
        from fastembed import TextEmbedding
        MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _model = TextEmbedding(EMBEDDING_MODEL, cache_dir=str(MODEL_CACHE_DIR))
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed a batch of texts -> (n, 384) float32, L2-normalised."""
    vectors = np.array(list(get_model().embed(texts)), dtype=np.float32)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def embed_query(text: str) -> np.ndarray:
    return embed_texts([text])[0]
