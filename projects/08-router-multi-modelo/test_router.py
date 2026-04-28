"""Testes do roteador multi-modelo."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import LLMResponse, MockLLMClient

# Import after path setup
from main import ModelSpec, Policy, build_client, choose, estimate_cost, load_policy


@pytest.fixture
def sample_policy():
    return Policy(
        defaults={"task": "simple", "max_cost_usd": 0.01},
        models=[
            ModelSpec(name="cheap-model", provider="openai", cost_per_1k_in=0.0001, cost_per_1k_out=0.0003, quality=0.5),
            ModelSpec(name="mid-model", provider="gemini", cost_per_1k_in=0.001, cost_per_1k_out=0.003, quality=0.75),
            ModelSpec(name="expensive-model", provider="anthropic", cost_per_1k_in=0.01, cost_per_1k_out=0.05, quality=0.95),
        ],
        routing={"simple": "cheapest_within_budget", "complex": "highest_quality_within_budget"},
    )


def test_load_policy_returns_valid():
    policy = load_policy()
    assert isinstance(policy, Policy)
    assert len(policy.models) > 0
    assert "simple" in policy.routing


def test_estimate_cost_short_prompt():
    spec = ModelSpec(name="m", provider="x", cost_per_1k_in=0.001, cost_per_1k_out=0.002, quality=0.5)
    cost = estimate_cost(spec, "hi")
    assert cost > 0
    assert isinstance(cost, float)


def test_estimate_cost_scales_with_length():
    spec = ModelSpec(name="m", provider="x", cost_per_1k_in=0.001, cost_per_1k_out=0.002, quality=0.5)
    short = estimate_cost(spec, "hello")
    long = estimate_cost(spec, "hello " * 1000)
    assert long > short


def test_choose_cheapest_within_budget(sample_policy):
    chosen = choose(sample_policy, "simple", max_cost=1.0, prompt="test prompt")
    assert chosen.name == "cheap-model"


def test_choose_highest_quality_within_budget(sample_policy):
    chosen = choose(sample_policy, "complex", max_cost=1.0, prompt="test prompt")
    assert chosen.name == "expensive-model"


def test_choose_falls_back_when_all_exceed_budget(sample_policy):
    chosen = choose(sample_policy, "simple", max_cost=0.0, prompt="test prompt")
    # Should pick cheapest overall as fallback
    assert chosen.name == "cheap-model"


def test_choose_empty_prompt(sample_policy):
    chosen = choose(sample_policy, "simple", max_cost=1.0, prompt="")
    assert chosen is not None


def test_build_client_no_keys():
    with patch.dict("os.environ", {}, clear=True):
        spec = ModelSpec(name="gpt-4o-mini", provider="openai", cost_per_1k_in=0.001, cost_per_1k_out=0.002, quality=0.7)
        client = build_client(spec)
        assert client is None


def test_build_client_unknown_provider():
    spec = ModelSpec(name="x", provider="unknown", cost_per_1k_in=0.0, cost_per_1k_out=0.0, quality=0.0)
    assert build_client(spec) is None


def test_mock_fallback():
    mock = MockLLMClient()
    resp = mock.complete("test")
    assert isinstance(resp, LLMResponse)
    assert "mock" in resp.text.lower() or "mock" in resp.provider
