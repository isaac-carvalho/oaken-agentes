"""Testes unitários do framework de eval — rodam offline com MockLLMClient."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import MockLLMClient

from main import CaseResult, PromptVariant, Suite, TestCase, render_report, run_suite


@pytest.fixture(autouse=True)
def _use_mock(monkeypatch):
    monkeypatch.setattr("main.get_default_client", lambda: MockLLMClient())


def _make_suite():
    return Suite(
        name="test_suite",
        prompts=[
            PromptVariant(id="v1", system="Classifique como positivo ou negativo."),
            PromptVariant(id="v2", system="Diga: positivo ou negativo."),
        ],
        cases=[
            TestCase(input="Adorei o produto!", expected="positivo"),
            TestCase(input="Péssimo atendimento", expected="negativo"),
        ],
    )


def test_suite_model_validates():
    s = _make_suite()
    assert s.name == "test_suite"
    assert len(s.prompts) == 2
    assert len(s.cases) == 2


def test_suite_invalid_missing_fields():
    with pytest.raises(Exception):
        Suite.model_validate({"name": "x"})


def test_run_suite_returns_all_variants():
    suite = _make_suite()
    results = run_suite(suite)
    assert set(results.keys()) == {"v1", "v2"}


def test_run_suite_result_counts():
    suite = _make_suite()
    results = run_suite(suite)
    for items in results.values():
        assert len(items) == 2


def test_run_suite_latency_non_negative():
    suite = _make_suite()
    results = run_suite(suite)
    for items in results.values():
        for r in items:
            assert r.latency_ms >= 0


def test_case_result_fields():
    suite = _make_suite()
    results = run_suite(suite)
    r = results["v1"][0]
    assert isinstance(r, CaseResult)
    assert r.case_input == "Adorei o produto!"
    assert r.expected == "positivo"
    assert isinstance(r.actual, str)


def test_render_report_markdown():
    suite = _make_suite()
    results = run_suite(suite)
    md = render_report(suite, results)
    assert md.startswith("# Eval —")
    assert "## v1" in md
    assert "## v2" in md
    assert "| input |" in md


def test_render_report_empty_suite():
    suite = Suite(name="vazio", prompts=[], cases=[])
    results = run_suite(suite)
    md = render_report(suite, results)
    assert "# Eval — vazio" in md
