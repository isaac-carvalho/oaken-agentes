"""Testes do benchmark LLMs."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import LLMResponse, MockLLMClient

from app import TASKS, build_clients, call_ollama


def test_tasks_not_empty():
    assert len(TASKS) >= 3
    for name, prompt in TASKS.items():
        assert isinstance(name, str) and len(name) > 0
        assert isinstance(prompt, str) and len(prompt) > 0


def test_build_clients_no_keys():
    with patch.dict("os.environ", {}, clear=True):
        clients = build_clients()
        assert "mock" in clients
        assert isinstance(clients["mock"], MockLLMClient)


def test_build_clients_with_openai_key():
    with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-fake-key-for-testing-only"}, clear=True):
        with patch("app.OpenAIClient") as mock_cls:
            mock_cls.return_value = MagicMock()
            clients = build_clients()
            assert "openai/gpt-4o-mini" in clients


def test_call_ollama_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"response": "Hello from ollama"}
    mock_resp.raise_for_status = MagicMock()
    with patch("app.requests.post", return_value=mock_resp):
        result = call_ollama("llama3.2", "test prompt")
        assert result.text == "Hello from ollama"
        assert result.provider == "ollama"
        assert result.model == "llama3.2"


def test_call_ollama_empty_response():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {}
    mock_resp.raise_for_status = MagicMock()
    with patch("app.requests.post", return_value=mock_resp):
        result = call_ollama("llama3.2", "test")
        assert result.text == ""


def test_call_ollama_network_error():
    with patch("app.requests.post", side_effect=ConnectionError("offline")):
        with pytest.raises(ConnectionError):
            call_ollama("llama3.2", "test")


def test_mock_client_complete():
    client = MockLLMClient()
    resp = client.complete("Resuma algo")
    assert isinstance(resp, LLMResponse)
    assert len(resp.text) > 0
    assert resp.provider == "mock"
