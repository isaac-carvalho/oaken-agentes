"""Embedder com fallback offline (HashEmbedder) quando HuggingFace é inacessível."""
from __future__ import annotations

import hashlib
import logging

log = logging.getLogger(__name__)


class _HashEmbedder:
    """Fallback determinístico: feature hashing 384d. Garante pipeline operacional sem internet."""

    def __init__(self, dim: int = 384) -> None:
        self.dim = dim

    def name(self) -> str:
        return "hash-embedder-384"

    def _embed_one(self, text: str) -> list[float]:
        v = [0.0] * self.dim
        for word in text.lower().split():
            idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % self.dim
            v[idx] += 1.0
        norm = sum(x * x for x in v) ** 0.5
        return [x / norm for x in v] if norm > 0 else v

    def __call__(self, input):
        return [self._embed_one(t) for t in input]

    def embed_documents(self, input):
        return self.__call__(input)

    def embed_query(self, input):
        if isinstance(input, str):
            return self._embed_one(input)
        return [self._embed_one(t) for t in input]


def get_embedder():
    """Tenta sentence-transformers; cai no HashEmbedder se HF estiver inacessível."""
    try:
        from chromadb.utils import embedding_functions

        emb = embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
        emb(["warmup"])  # força download/carregamento agora
        return emb
    except Exception:
        return _HashEmbedder()
