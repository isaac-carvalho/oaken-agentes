"""Testes unitários do agente ReAct — rodam offline."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import LLMResponse, MockLLMClient

from main import (
    TOOL_REGISTRY,
    parse_action,
    validate_action,
    _build_system_prompt,
)


# --- parse_action ---

def test_parse_action_valid():
    text = 'PENSAMENTO: preciso calcular\nACAO: {"tool": "calc", "input": "2+2"}'
    action = parse_action(text)
    assert action == {"tool": "calc", "input": "2+2"}


def test_parse_action_no_action():
    text = "PENSAMENTO: vou pensar mais\nFINAL: resposta"
    assert parse_action(text) is None


def test_parse_action_malformed_json():
    text = 'ACAO: {"tool": "calc", "input": "2+2"} extra text here'
    action = parse_action(text)
    assert action is not None
    assert action["tool"] == "calc"


def test_parse_action_broken_json():
    text = 'ACAO: {not valid json at all'
    assert parse_action(text) is None


def test_parse_action_nested_braces():
    text = 'ACAO: {"tool": "python", "input": "print({1: 2})"}'
    action = parse_action(text)
    assert action is not None
    assert action["tool"] == "python"


# --- validate_action ---

def test_validate_action_valid():
    assert validate_action({"tool": "calc", "input": "1+1"}) is None


def test_validate_action_missing_tool():
    err = validate_action({"input": "1+1"})
    assert err is not None
    assert "tool" in err.lower()


def test_validate_action_unknown_tool():
    err = validate_action({"tool": "nonexistent", "input": "x"})
    assert err is not None
    assert "desconhecida" in err


def test_validate_action_missing_input():
    err = validate_action({"tool": "calc"})
    assert err is not None
    assert "input" in err.lower()


# --- TOOL_REGISTRY ---

def test_tool_registry_has_all_tools():
    assert "calc" in TOOL_REGISTRY
    assert "web" in TOOL_REGISTRY
    assert "python" in TOOL_REGISTRY


def test_tool_registry_entries_have_fn_and_desc():
    for name, info in TOOL_REGISTRY.items():
        assert "fn" in info
        assert "description" in info
        assert callable(info["fn"])


# --- _build_system_prompt ---

def test_system_prompt_mentions_tools():
    prompt = _build_system_prompt()
    assert "calc" in prompt
    assert "web" in prompt
    assert "python" in prompt
    assert "ACAO" in prompt
    assert "FINAL" in prompt


# --- CLI via Typer ---

def test_main_final_response(monkeypatch):
    """Agente que responde FINAL imediatamente."""
    class DirectClient:
        provider = "direct"
        def complete(self, prompt, *, system=None, model=None):
            return LLMResponse(text="FINAL: 42", model="m", provider="direct")

    monkeypatch.setattr("main.get_default_client", lambda: DirectClient())

    from typer.testing import CliRunner
    from main import app

    runner = CliRunner()
    result = runner.invoke(app, ["Quanto é 6*7?"])
    assert result.exit_code == 0
    assert "42" in result.output


def test_main_max_iter_limit(monkeypatch):
    """Agente que nunca diz FINAL — deve parar no limite."""
    class LoopClient:
        provider = "loop"
        def complete(self, prompt, *, system=None, model=None):
            return LLMResponse(text="PENSAMENTO: pensando...", model="m", provider="loop")

    monkeypatch.setattr("main.get_default_client", lambda: LoopClient())

    from typer.testing import CliRunner
    from main import app

    runner = CliRunner()
    result = runner.invoke(app, ["teste", "--max-iter", "2"])
    assert "sem ação parseável" in result.output or "limite" in result.output
