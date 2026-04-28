"""Tests for _shared/llm_clients.py."""
from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from llm_clients import (
    LLMResponse,
    MockLLMClient,
    get_default_client,
)


def test_llm_response_dataclass():
    r = LLMResponse(text="hi", model="m", provider="p")
    assert r.text == "hi"
    assert r.usage is None


def test_mock_client_deterministic():
    c = MockLLMClient()
    r1 = c.complete("test prompt")
    r2 = c.complete("test prompt")
    assert r1.text == r2.text
    assert r1.provider == "mock"


def test_mock_client_different_prompts():
    c = MockLLMClient()
    r1 = c.complete("alpha")
    r2 = c.complete("beta")
    assert r1.text != r2.text


def test_mock_client_usage_info():
    c = MockLLMClient()
    r = c.complete("hello world")
    assert r.usage is not None
    assert r.usage["prompt"] == len("hello world")


def test_get_default_client_no_keys():
    """Without API keys, should return MockLLMClient."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY")}
    with patch.dict(os.environ, env, clear=True):
        client = get_default_client()
        assert client.provider == "mock"


def test_mock_client_with_system():
    c = MockLLMClient()
    r = c.complete("test", system="You are helpful")
    assert r.text  # should produce output regardless of system
    assert r.model == "mock-1"
