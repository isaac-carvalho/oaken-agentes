"""Framework de A/B testing de prompts."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import typer
import yaml
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

app = typer.Typer()


class PromptVariant(BaseModel):
    id: str
    system: str


class TestCase(BaseModel):
    input: str
    expected: str


class Suite(BaseModel):
    name: str
    prompts: list[PromptVariant]
    cases: list[TestCase]


class CaseResult(BaseModel):
    case_input: str
    expected: str
    actual: str
    correct: bool
    latency_ms: int
    tokens: int


def run_suite(suite: Suite) -> dict[str, list[CaseResult]]:
    client = get_default_client()
    results: dict[str, list[CaseResult]] = {}
    for variant in suite.prompts:
        per_variant: list[CaseResult] = []
        for case in suite.cases:
            t0 = time.perf_counter()
            resp = client.complete(case.input, system=variant.system)
            elapsed = int((time.perf_counter() - t0) * 1000)
            actual = resp.text.strip().splitlines()[0] if resp.text else ""
            tokens = (resp.usage or {}).get("completion", 0) + (resp.usage or {}).get("prompt", 0)
            per_variant.append(
                CaseResult(
                    case_input=case.input,
                    expected=case.expected,
                    actual=actual,
                    correct=case.expected.lower() in actual.lower(),
                    latency_ms=elapsed,
                    tokens=tokens,
                )
            )
        results[variant.id] = per_variant
    return results


def render_report(suite: Suite, results: dict[str, list[CaseResult]]) -> str:
    lines = [f"# Eval — {suite.name}", ""]
    for variant_id, items in results.items():
        acc = sum(1 for r in items if r.correct) / max(len(items), 1)
        avg_lat = sum(r.latency_ms for r in items) / max(len(items), 1)
        total_tok = sum(r.tokens for r in items)
        lines.append(f"## {variant_id} — acerto={acc:.0%}, latência média={avg_lat:.0f}ms, tokens={total_tok}")
        lines.append("")
        lines.append("| input | esperado | obtido | ok |")
        lines.append("|---|---|---|---|")
        for r in items:
            ok = "✅" if r.correct else "❌"
            lines.append(f"| {r.case_input} | {r.expected} | {r.actual} | {ok} |")
        lines.append("")
    return "\n".join(lines)


@app.command()
def main(suite_path: Path) -> None:
    raw = yaml.safe_load(suite_path.read_text(encoding="utf-8"))
    suite = Suite.model_validate(raw)
    results = run_suite(suite)
    out = suite_path.with_suffix(".report.md")
    out.write_text(render_report(suite, results), encoding="utf-8")
    typer.echo(f"Relatório salvo em {out}")


if __name__ == "__main__":
    app()
