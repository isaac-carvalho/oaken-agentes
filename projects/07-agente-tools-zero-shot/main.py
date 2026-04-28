"""Agente ReAct com 3 tools (calc, web, python)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import typer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

app = typer.Typer()


def tool_calc(expr: str) -> str:
    import numexpr

    return str(numexpr.evaluate(expr).item())


def tool_web(query: str) -> str:
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        return "\n".join(f"- {r['title']}: {r['body']}" for r in results) or "sem resultados"
    except Exception as e:
        return f"erro web: {e}"


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


TOOLS = {
    "calc": (tool_calc, "Calculadora numérica. Input: expressão como '2*pi*3.5'."),
    "web": (tool_web, "Busca web. Input: termo de busca."),
    "python": (tool_python, "Executa código Python. Input: código."),
}

SYSTEM = (
    "Você é um agente que resolve perguntas usando ferramentas.\n"
    f"Ferramentas disponíveis:\n"
    + "\n".join(f"- {n}: {d[1]}" for n, d in TOOLS.items())
    + "\n\nA cada turno responda em UMA destas formas:\n"
    'PENSAMENTO: ...\nACAO: {"tool": "<nome>", "input": "<arg>"}\n'
    "ou\nFINAL: <resposta final em português>\n"
)

ACTION_RE = re.compile(r"ACAO:\s*(\{.*\})", re.DOTALL)


@app.command()
def main(pergunta: str, max_iter: int = 6) -> None:
    client = get_default_client()
    history = pergunta
    for step in range(max_iter):
        resp = client.complete(history, system=SYSTEM).text
        typer.echo(f"--- step {step} ---\n{resp}")
        if "FINAL:" in resp:
            typer.echo("\n>>> " + resp.split("FINAL:", 1)[1].strip())
            return
        m = ACTION_RE.search(resp)
        if not m:
            typer.echo("(sem ação parseável, encerrando)")
            return
        try:
            action = json.loads(m.group(1))
        except json.JSONDecodeError:
            typer.echo("(JSON inválido, encerrando)")
            return
        fn, _ = TOOLS.get(action.get("tool"), (None, None))
        if not fn:
            obs = f"tool inválida: {action.get('tool')}"
        else:
            obs = fn(action.get("input", ""))
        typer.echo(f"OBSERVACAO: {obs}\n")
        history += f"\n{resp}\nOBSERVACAO: {obs}\n"
    typer.echo("(limite de iterações atingido)")


if __name__ == "__main__":
    app()
