"""Agente ReAct com 3 tools (calc, web, python)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import typer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

app = typer.Typer()

# --- Tool definitions ---

TOOL_REGISTRY: dict[str, dict[str, Any]] = {}


def register_tool(name: str, description: str):
    """Decorator para registrar ferramentas no agente."""
    def decorator(fn):
        TOOL_REGISTRY[name] = {"fn": fn, "description": description}
        return fn
    return decorator


@register_tool("calc", "Calculadora numérica. Input: expressão como '2*pi*3.5'.")
def tool_calc(expr: str) -> str:
    import numexpr
    return str(numexpr.evaluate(expr).item())


@register_tool("web", "Busca web. Input: termo de busca.")
def tool_web(query: str) -> str:
    try:
        try:
            from ddgs import DDGS  # type: ignore
        except ImportError:
            from duckduckgo_search import DDGS  # type: ignore (lib antiga)

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        return "\n".join(f"- {r.get('title','?')}: {r.get('body','')}" for r in results) or "sem resultados"
    except Exception as e:
        return f"erro web: {e}"


@register_tool("python", "Executa código Python. Input: código.")
def tool_python(code: str) -> str:
    try:
        out = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return (out.stdout or out.stderr).strip()[:1000]
    except Exception as e:
        return f"erro: {e}"


# Backward compat
TOOLS = {name: (info["fn"], info["description"]) for name, info in TOOL_REGISTRY.items()}


def _build_system_prompt() -> str:
    tool_lines = "\n".join(f"- {n}: {info['description']}" for n, info in TOOL_REGISTRY.items())
    return (
        "Você é um agente que resolve perguntas usando ferramentas.\n"
        f"Ferramentas disponíveis:\n{tool_lines}\n\n"
        "A cada turno responda em UMA destas formas:\n"
        'PENSAMENTO: ...\nACAO: {"tool": "<nome>", "input": "<arg>"}\n'
        "ou\nFINAL: <resposta final em português>\n"
    )


SYSTEM = _build_system_prompt()

ACTION_RE = re.compile(r"ACAO:\s*(\{.*\})", re.DOTALL)


def parse_action(text: str) -> dict | None:
    """Extrai a ação JSON da resposta do LLM com fallback robusto."""
    m = ACTION_RE.search(text)
    if not m:
        return None

    raw = m.group(1).strip()
    # Tenta parse direto
    try:
        action = json.loads(raw)
        if isinstance(action, dict):
            return action
    except json.JSONDecodeError:
        pass

    # Fallback: tenta encontrar JSON válido dentro do texto
    # (LLMs às vezes adicionam texto depois do JSON)
    brace_count = 0
    start = None
    for i, ch in enumerate(raw):
        if ch == "{":
            if start is None:
                start = i
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if brace_count == 0 and start is not None:
                candidate = raw[start:i + 1]
                try:
                    action = json.loads(candidate)
                    if isinstance(action, dict):
                        return action
                except json.JSONDecodeError:
                    continue

    return None


def validate_action(action: dict) -> str | None:
    """Valida a ação extraída. Retorna mensagem de erro ou None se válida."""
    if "tool" not in action:
        return "Ação sem campo 'tool'"
    if action["tool"] not in TOOL_REGISTRY:
        available = ", ".join(TOOL_REGISTRY.keys())
        return f"Tool '{action['tool']}' desconhecida. Disponíveis: {available}"
    if "input" not in action:
        return "Ação sem campo 'input'"
    return None


DEFAULT_MAX_ITER = 6


@app.command()
def main(pergunta: str, max_iter: int = DEFAULT_MAX_ITER) -> None:
    if max_iter < 1:
        typer.echo("Erro: max_iter deve ser >= 1", err=True)
        raise typer.Exit(code=1)
    if max_iter > 20:
        typer.echo("Aviso: max_iter limitado a 20", err=True)
        max_iter = 20

    client = get_default_client()
    history = pergunta
    for step in range(max_iter):
        resp = client.complete(history, system=SYSTEM).text
        typer.echo(f"--- step {step} ---\n{resp}")

        if "FINAL:" in resp:
            typer.echo("\n>>> " + resp.split("FINAL:", 1)[1].strip())
            return

        action = parse_action(resp)
        if action is None:
            typer.echo("(sem ação parseável, encerrando)")
            return

        error = validate_action(action)
        if error:
            obs = f"ERRO: {error}"
        else:
            fn = TOOL_REGISTRY[action["tool"]]["fn"]
            obs = fn(action.get("input", ""))

        typer.echo(f"OBSERVACAO: {obs}\n")
        history += f"\n{resp}\nOBSERVACAO: {obs}\n"

    typer.echo("(limite de iterações atingido)")


if __name__ == "__main__":
    app()
