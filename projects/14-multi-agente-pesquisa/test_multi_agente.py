"""Testes do sistema multi-agente pesquisa."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import LLMResponse

from main import State, _search, critic, increment, researcher, should_iterate, writer


# --- _search ---

def test_search_offline_fallback():
    """Sem duckduckgo_search instalado, deve retornar mensagem de erro/offline."""
    with patch.dict("sys.modules", {"ddgs": None, "duckduckgo_search": None}):
        result = _search("inteligência artificial")
        assert "offline" in result.lower() or "erro" in result.lower()


def test_search_returns_string():
    mock_ddgs_instance = MagicMock()
    mock_ddgs_instance.__enter__ = MagicMock(return_value=mock_ddgs_instance)
    mock_ddgs_instance.__exit__ = MagicMock(return_value=False)
    mock_ddgs_instance.text.return_value = [{"title": "Resultado", "body": "Conteúdo"}]

    mock_module = MagicMock()
    mock_module.DDGS.return_value = mock_ddgs_instance

    with patch.dict("sys.modules", {"ddgs": mock_module}):
        result = _search("IA")
        assert "Resultado" in result


# --- researcher ---

def test_researcher_generates_findings():
    mock_client = MagicMock()
    mock_client.complete.return_value = LLMResponse(
        text="1. Sub-tópico A\n2. Sub-tópico B\n3. Sub-tópico C\n4. Sub-tópico D",
        model="m", provider="mock"
    )
    with patch("main.get_default_client", return_value=mock_client), \
         patch("main._search", return_value="resultado mock"):
        result = researcher({"topic": "IA generativa", "research": "", "critique": "", "iterations": 0, "report": ""})
        assert "research" in result
        assert len(result["research"]) > 0


# --- critic ---

def test_critic_returns_ok():
    mock_client = MagicMock()
    mock_client.complete.return_value = LLMResponse(text="OK, está completo", model="m", provider="mock")
    with patch("main.get_default_client", return_value=mock_client):
        result = critic({"topic": "IA", "research": "dados bons", "critique": "", "iterations": 0, "report": ""})
        assert "OK" in result["critique"]


def test_critic_returns_improvement():
    mock_client = MagicMock()
    mock_client.complete.return_value = LLMResponse(
        text="- Falta dados sobre custos\n- Adicionar exemplos", model="m", provider="mock"
    )
    with patch("main.get_default_client", return_value=mock_client):
        result = critic({"topic": "IA", "research": "dados parciais", "critique": "", "iterations": 0, "report": ""})
        assert "Falta" in result["critique"]


# --- should_iterate ---

def test_should_iterate_stops_on_ok():
    state: State = {"topic": "t", "research": "r", "critique": "OK tudo bem", "iterations": 0, "report": ""}
    assert should_iterate(state) == "writer"


def test_should_iterate_continues_on_criticism():
    state: State = {"topic": "t", "research": "r", "critique": "Falta info", "iterations": 0, "report": ""}
    assert should_iterate(state) == "researcher"


def test_should_iterate_stops_at_max_iterations():
    """Com max_iterations=3, deve parar quando iterations >= 3."""
    state: State = {"topic": "t", "research": "r", "critique": "Falta info", "iterations": 3, "report": ""}
    assert should_iterate(state) == "writer"


def test_should_iterate_allows_iteration_2():
    """Iteração 2 (< 3) ainda deve permitir continuar."""
    state: State = {"topic": "t", "research": "r", "critique": "Precisa melhorar", "iterations": 2, "report": ""}
    assert should_iterate(state) == "researcher"


# --- increment ---

def test_increment():
    result = increment({"topic": "", "research": "", "critique": "", "iterations": 0, "report": ""})
    assert result["iterations"] == 1


def test_increment_from_2():
    result = increment({"topic": "", "research": "", "critique": "", "iterations": 2, "report": ""})
    assert result["iterations"] == 3


# --- writer ---

def test_writer_produces_report():
    mock_client = MagicMock()
    mock_client.complete.return_value = LLMResponse(text="# Relatório\nConteúdo aqui", model="m", provider="mock")
    with patch("main.get_default_client", return_value=mock_client):
        result = writer({"topic": "IA", "research": "dados", "critique": "OK", "iterations": 1, "report": ""})
        assert "report" in result
        assert len(result["report"]) > 0
