"""Roteador multi-modelo com política declarativa."""
from __future__ import annotations

import sys
from pathlib import Path

import typer
import yaml
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.env import get_env  # noqa: E402
from projects._shared.llm_clients import (  # noqa: E402
    AnthropicClient,
    GeminiClient,
    MockLLMClient,
    OpenAIClient,
)

app = typer.Typer()


class ModelSpec(BaseModel):
    name: str
    provider: str
    cost_per_1k_in: float
    cost_per_1k_out: float
    quality: float


class Policy(BaseModel):
    defaults: dict
    models: list[ModelSpec]
    routing: dict[str, str]


def load_policy() -> Policy:
    raw = yaml.safe_load((Path(__file__).parent / "policies.yaml").read_text(encoding="utf-8"))
    return Policy.model_validate(raw)


def estimate_cost(spec: ModelSpec, prompt: str) -> float:
    in_tok = max(len(prompt) // 4, 1)
    return (in_tok / 1000) * spec.cost_per_1k_in + (200 / 1000) * spec.cost_per_1k_out


def choose(policy: Policy, task: str, max_cost: float, prompt: str) -> ModelSpec:
    candidates = [m for m in policy.models if estimate_cost(m, prompt) <= max_cost]
    if not candidates:
        candidates = sorted(policy.models, key=lambda m: estimate_cost(m, prompt))[:1]
    strategy = policy.routing.get(task, "cheapest_within_budget")
    if strategy == "highest_quality_within_budget":
        return max(candidates, key=lambda m: m.quality)
    return min(candidates, key=lambda m: estimate_cost(m, prompt))


def build_client(spec: ModelSpec):
    if spec.provider == "openai":
        key = get_env("OPENAI_API_KEY")
        return OpenAIClient(key, default_model=spec.name) if key else None
    if spec.provider == "gemini":
        key = get_env("GEMINI_API_KEY") or get_env("GOOGLE_API_KEY")
        return GeminiClient(key, default_model=spec.name) if key else None
    if spec.provider == "anthropic":
        key = get_env("ANTHROPIC_API_KEY")
        return AnthropicClient(key, default_model=spec.name) if key else None
    return None


@app.command()
def main(
    prompt: str,
    task: str = typer.Option("simple", help="simple | complex"),
    max_cost: float = typer.Option(0.01),
) -> None:
    policy = load_policy()
    chosen = choose(policy, task, max_cost, prompt)
    typer.echo(f"[router] escolhido: {chosen.name} ({chosen.provider}) — custo estimado ~${estimate_cost(chosen, prompt):.5f}")
    client = build_client(chosen)
    if client is None:
        typer.echo("[router] sem API key — usando MockLLMClient")
        client = MockLLMClient()
    try:
        resp = client.complete(prompt)
    except Exception as e:
        typer.echo(f"[router] falhou ({e}), fallback para mock")
        resp = MockLLMClient().complete(prompt)
    typer.echo("\n" + resp.text)


if __name__ == "__main__":
    app()
