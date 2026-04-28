"""Testes unitários do framework (rodam sem API key, com MockLLMClient)."""
from pathlib import Path

import yaml

from main import Suite, render_report, run_suite


def test_suite_loads_yaml():
    raw = yaml.safe_load(Path("suites/sentimento.yaml").read_text(encoding="utf-8"))
    suite = Suite.model_validate(raw)
    assert suite.name == "sentimento_pt"
    assert len(suite.prompts) == 2
    assert len(suite.cases) >= 2


def test_run_suite_produces_results():
    raw = yaml.safe_load(Path("suites/sentimento.yaml").read_text(encoding="utf-8"))
    suite = Suite.model_validate(raw)
    results = run_suite(suite)
    assert set(results) == {"v1", "v2"}
    for items in results.values():
        assert len(items) == len(suite.cases)
        assert all(r.latency_ms >= 0 for r in items)


def test_render_report_returns_markdown():
    raw = yaml.safe_load(Path("suites/sentimento.yaml").read_text(encoding="utf-8"))
    suite = Suite.model_validate(raw)
    results = run_suite(suite)
    md = render_report(suite, results)
    assert md.startswith("# Eval —")
    assert "| input |" in md
