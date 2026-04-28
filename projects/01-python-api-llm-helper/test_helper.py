"""Testes unitários do CLI helper — rodam offline com mock."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import LLMResponse, MockLLMClient


# Importa depois de ajustar sys.path
from main import (
    LLMRequestError,
    _ask_with_retry,
    estimate_tokens,
)


@pytest.fixture(autouse=True)
def _mock_client(monkeypatch):
    """Garante que get_default_client retorna MockLLMClient."""
    monkeypatch.setattr("main.get_default_client", lambda: MockLLMClient())


# --- estimate_tokens ---

def test_estimate_tokens_basic():
    assert estimate_tokens("hello world") >= 1


def test_estimate_tokens_empty():
    assert estimate_tokens("") == 1


def test_estimate_tokens_long():
    text = "a" * 400
    assert estimate_tokens(text) == 100


# --- _ask_with_retry ---

def test_ask_with_retry_success():
    result = _ask_with_retry("system", "prompt")
    assert isinstance(result, str)
    assert len(result) > 0


def test_ask_with_retry_retries_on_failure(monkeypatch):
    """Deve tentar novamente e eventualmente ter sucesso."""
    call_count = 0

    class FlakeyClient:
        provider = "flakey"

        def complete(self, prompt, *, system=None, model=None):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("timeout")
            return LLMResponse(text="ok", model="m", provider="flakey")

    monkeypatch.setattr("main.get_default_client", lambda: FlakeyClient())
    # Sem delay real nos testes
    monkeypatch.setattr("main.BASE_DELAY", 0.0)
    result = _ask_with_retry("sys", "prompt", max_retries=3)
    assert result == "ok"
    assert call_count == 3


def test_ask_with_retry_exhausts_retries(monkeypatch):
    class BrokenClient:
        provider = "broken"

        def complete(self, prompt, *, system=None, model=None):
            raise RuntimeError("always fails")

    monkeypatch.setattr("main.get_default_client", lambda: BrokenClient())
    monkeypatch.setattr("main.BASE_DELAY", 0.0)
    with pytest.raises(LLMRequestError, match="Falha após 3 tentativas"):
        _ask_with_retry("sys", "prompt", max_retries=3)


# --- CLI commands via Typer ---

def test_resumir_empty_text():
    from typer.testing import CliRunner
    from main import app

    runner = CliRunner()
    result = runner.invoke(app, ["resumir", "   "])
    assert result.exit_code != 0


def test_resumir_ok():
    from typer.testing import CliRunner
    from main import app

    runner = CliRunner()
    result = runner.invoke(app, ["resumir", "Este é um texto para resumir"])
    assert result.exit_code == 0
    assert "mock-llm" in result.output or "simulada" in result.output


def test_traduzir_ok():
    from typer.testing import CliRunner
    from main import app

    runner = CliRunner()
    result = runner.invoke(app, ["traduzir", "Olá mundo"])
    assert result.exit_code == 0


def test_codigo_empty_desc():
    from typer.testing import CliRunner
    from main import app

    runner = CliRunner()
    result = runner.invoke(app, ["codigo", ""])
    assert result.exit_code != 0
