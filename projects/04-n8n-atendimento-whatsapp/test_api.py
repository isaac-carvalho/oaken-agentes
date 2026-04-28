"""Testes unitários da API de atendimento — rodam offline."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import LLMResponse, MockLLMClient

# Patch antes de importar api (que instancia _llm no topo)
with patch("projects._shared.llm_clients.get_default_client", return_value=MockLLMClient()):
    with patch.dict("sys.modules", {}):
        pass
    import api

from fastapi.testclient import TestClient

client = TestClient(api.app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "provider" in data


def test_atender_basic():
    resp = client.post("/atender", json={
        "telefone": "+5511999999999",
        "mensagem": "Olá, bom dia!",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "intencao" in data
    assert "resposta" in data
    assert "provider" in data
    assert data["intencao"] in ("saudacao", "duvida", "reclamacao", "outro")


def test_atender_missing_fields():
    resp = client.post("/atender", json={"telefone": "+5511999999999"})
    assert resp.status_code == 422  # Validation error


def test_atender_empty_message():
    resp = client.post("/atender", json={
        "telefone": "+5511999999999",
        "mensagem": "",
    })
    # Deve funcionar mesmo com mensagem vazia (o LLM classifica como "outro")
    assert resp.status_code == 200
    data = resp.json()
    assert data["intencao"] in ("saudacao", "duvida", "reclamacao", "outro")


def test_atender_intencao_fallback():
    """Se a resposta do LLM não contiver nenhuma intenção conhecida, deve cair em 'outro'."""
    resp = client.post("/atender", json={
        "telefone": "+5511999999999",
        "mensagem": "xyz123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["intencao"] in ("saudacao", "duvida", "reclamacao", "outro")


def test_intencoes_constant():
    assert len(api.INTENCOES) == 4
    assert "outro" in api.INTENCOES
