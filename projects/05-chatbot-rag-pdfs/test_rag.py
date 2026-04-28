"""Testes unitários do chatbot RAG — rodam offline sem Streamlit."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# Importar funções puras sem disparar o Streamlit UI
# Precisamos simular st antes de importar app
from unittest.mock import MagicMock

sys.modules["streamlit"] = MagicMock()

from app import _HashEmbedder, chunk_text


# --- chunk_text ---

def test_chunk_text_basic():
    text = "a" * 2000
    chunks = chunk_text(text, size=800, overlap=100)
    assert len(chunks) >= 2
    assert chunks[0] == "a" * 800


def test_chunk_text_short():
    chunks = chunk_text("hello", size=800, overlap=100)
    assert len(chunks) == 1
    assert chunks[0] == "hello"


def test_chunk_text_empty():
    chunks = chunk_text("", size=800, overlap=100)
    assert chunks == []


def test_chunk_text_overlap_continuity():
    text = "abcdefghij" * 100  # 1000 chars
    chunks = chunk_text(text, size=400, overlap=50)
    # Verificar que overlap funciona: final de chunk N aparece no início de chunk N+1
    for i in range(len(chunks) - 1):
        tail = chunks[i][-50:]
        head = chunks[i + 1][:50]
        assert tail == head


def test_chunk_text_custom_sizes():
    text = "x" * 100
    chunks = chunk_text(text, size=30, overlap=10)
    assert len(chunks) == 5  # ceil(100/20)


# --- _HashEmbedder ---

def test_hash_embedder_dimensions():
    emb = _HashEmbedder(dim=128)
    vec = emb._embed_one("hello world")
    assert len(vec) == 128


def test_hash_embedder_normalized():
    emb = _HashEmbedder(dim=384)
    vec = emb._embed_one("teste de normalização")
    norm = sum(x * x for x in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-6


def test_hash_embedder_empty_string():
    emb = _HashEmbedder(dim=384)
    vec = emb._embed_one("")
    # String vazia não tem palavras -> vetor zero
    assert all(x == 0.0 for x in vec)


def test_hash_embedder_deterministic():
    emb = _HashEmbedder(dim=256)
    v1 = emb._embed_one("mesmo texto")
    v2 = emb._embed_one("mesmo texto")
    assert v1 == v2


def test_hash_embedder_call_batch():
    emb = _HashEmbedder(dim=128)
    result = emb(["hello", "world"])
    assert len(result) == 2
    assert len(result[0]) == 128


def test_hash_embedder_embed_query_str():
    emb = _HashEmbedder(dim=128)
    result = emb.embed_query("query")
    assert len(result) == 128
    assert isinstance(result[0], float)
