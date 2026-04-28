"""Testes do agente RAG LangGraph."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import LLMResponse

# Test embedder directly (no external deps needed)
from embedder import _HashEmbedder, get_embedder


# --- Embedder tests ---

def test_hash_embedder_dimension():
    emb = _HashEmbedder(dim=128)
    result = emb._embed_one("teste de embedding")
    assert len(result) == 128


def test_hash_embedder_normalized():
    emb = _HashEmbedder()
    vec = emb._embed_one("hello world")
    norm = sum(x * x for x in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-6


def test_hash_embedder_deterministic():
    emb = _HashEmbedder()
    v1 = emb._embed_one("reprodutível")
    v2 = emb._embed_one("reprodutível")
    assert v1 == v2


def test_hash_embedder_different_texts():
    emb = _HashEmbedder()
    v1 = emb._embed_one("gato")
    v2 = emb._embed_one("cão")
    assert v1 != v2


def test_hash_embedder_empty_string():
    emb = _HashEmbedder()
    vec = emb._embed_one("")
    assert len(vec) == 384
    # Empty string has no words → all zeros
    assert all(x == 0.0 for x in vec)


def test_hash_embedder_batch_call():
    emb = _HashEmbedder()
    results = emb(["hello", "world", "test"])
    assert len(results) == 3
    assert all(len(v) == 384 for v in results)


def test_hash_embedder_embed_documents():
    emb = _HashEmbedder()
    results = emb.embed_documents(["a", "b"])
    assert len(results) == 2


def test_hash_embedder_embed_query_string():
    emb = _HashEmbedder()
    result = emb.embed_query("single query")
    assert len(result) == 384
    assert isinstance(result[0], float)


def test_get_embedder_fallback():
    """Sem sentence-transformers, deve cair no HashEmbedder."""
    with patch.dict("sys.modules", {"chromadb.utils": None, "chromadb.utils.embedding_functions": None}):
        import importlib
        import embedder as emb_mod
        importlib.reload(emb_mod)
        result = emb_mod.get_embedder()
        assert type(result).__name__ == "_HashEmbedder"


# --- Agent node tests (mocked) ---

def test_retrieve_node_empty_collection():
    mock_coll = MagicMock()
    mock_coll.query.return_value = {"documents": [[]]}
    mock_chroma = MagicMock()
    mock_chroma.PersistentClient.return_value.get_or_create_collection.return_value = mock_coll

    with patch.dict("sys.modules", {"chromadb": mock_chroma}):
        from agent import _retrieve_node
        result = _retrieve_node({"question": "test", "messages": []})
        assert result["context"] == ""


def test_answer_node_returns_draft():
    mock_client = MagicMock()
    mock_client.complete.return_value = LLMResponse(text="Resposta rascunho", model="m", provider="mock")

    with patch("agent.get_default_client", return_value=mock_client):
        from agent import _answer_node
        result = _answer_node({"question": "O que é IA?", "context": "IA = inteligência artificial", "messages": []})
        assert result["draft"] == "Resposta rascunho"


def test_critic_node_returns_critique():
    mock_client = MagicMock()
    mock_client.complete.return_value = LLMResponse(text="OK, está bom", model="m", provider="mock")

    with patch("agent.get_default_client", return_value=mock_client):
        from agent import _critic_node
        result = _critic_node({"question": "q", "draft": "draft text", "messages": []})
        assert "OK" in result["critique"]


def test_refine_node_keeps_draft_on_ok():
    from agent import _refine_node
    result = _refine_node({
        "question": "q", "context": "c", "draft": "bom rascunho",
        "critique": "OK, está completo", "messages": []
    })
    assert result["final"] == "bom rascunho"


def test_refine_node_improves_on_criticism():
    mock_client = MagicMock()
    mock_client.complete.return_value = LLMResponse(text="Versão melhorada", model="m", provider="mock")

    with patch("agent.get_default_client", return_value=mock_client):
        from agent import _refine_node
        result = _refine_node({
            "question": "q", "context": "c", "draft": "rascunho ruim",
            "critique": "MELHORAR: falta detalhes", "messages": []
        })
        assert result["final"] == "Versão melhorada"
