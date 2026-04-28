"""Testes unitários dos módulos compartilhados — rodam offline."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import (
    LLMResponse,
    MockLLMClient,
    get_default_client,
)
from projects._shared.env import _load_dotenv_simple, get_env, require_env


# --- MockLLMClient ---

def test_mock_client_returns_response():
    client = MockLLMClient()
    resp = client.complete("hello")
    assert isinstance(resp, LLMResponse)
    assert resp.provider == "mock"
    assert "mock-llm" in resp.text


def test_mock_client_deterministic():
    client = MockLLMClient()
    r1 = client.complete("test", system="sys")
    r2 = client.complete("test", system="sys")
    assert r1.text == r2.text


def test_mock_client_different_prompts_differ():
    client = MockLLMClient()
    r1 = client.complete("aaa")
    r2 = client.complete("bbb")
    assert r1.text != r2.text


def test_mock_client_usage():
    client = MockLLMClient()
    resp = client.complete("test")
    assert resp.usage is not None
    assert "prompt" in resp.usage
    assert "completion" in resp.usage


# --- get_default_client ---

def test_get_default_client_falls_to_mock(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    client = get_default_client()
    assert client.provider == "mock"


# --- env ---

def test_load_dotenv_simple(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text('TEST_KEY_123="hello"\n# comment\nTEST_KEY_456=world\n')
    _load_dotenv_simple(env_file)
    assert os.environ.get("TEST_KEY_123") == "hello"
    assert os.environ.get("TEST_KEY_456") == "world"
    # Cleanup
    os.environ.pop("TEST_KEY_123", None)
    os.environ.pop("TEST_KEY_456", None)


def test_load_dotenv_missing_file(tmp_path):
    _load_dotenv_simple(tmp_path / "nonexistent")
    # Should not raise


def test_require_env_raises(monkeypatch):
    monkeypatch.delenv("NONEXISTENT_VAR_XYZ", raising=False)
    with pytest.raises(RuntimeError, match="ausente"):
        require_env("NONEXISTENT_VAR_XYZ")
