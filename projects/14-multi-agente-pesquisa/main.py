"""Sistema multi-agente: Pesquisador → Crítico → Escritor."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TypedDict

import typer
from langgraph.graph import END, START, StateGraph

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

app = typer.Typer()


class State(TypedDict):
    topic: str
    research: str
    critique: str
    iterations: int
    report: str


def _search(query: str, k: int = 5) -> str:
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            res = list(ddgs.text(query, max_results=k))
        return "\n".join(f"- {r['title']}: {r['body']}" for r in res)
    except Exception as e:
        return f"(busca offline ou erro: {e})"


def researcher(state: State) -> dict:
    llm = get_default_client()
    queries_text = llm.complete(
        f"Liste 4 sub-tópicos de pesquisa, um por linha, sobre: {state['topic']}",
        system="Você é um pesquisador metódico.",
    ).text
    findings: list[str] = []
    for line in queries_text.splitlines()[:4]:
        q = line.lstrip("-•0123456789. ").strip()
        if q:
            findings.append(f"### {q}\n{_search(q)}")
    return {"research": "\n\n".join(findings)}


def critic(state: State) -> dict:
    llm = get_default_client()
    prompt = (
        f"Tópico: {state['topic']}\n\nMaterial coletado:\n{state['research']}\n\n"
        "Aponte em até 3 bullets o que ainda falta para um relatório completo. "
        "Comece com OK se estiver satisfatório."
    )
    return {"critique": llm.complete(prompt, system="Você é um crítico exigente.").text}


def writer(state: State) -> dict:
    llm = get_default_client()
    prompt = (
        f"Escreva um relatório técnico em markdown sobre: {state['topic']}\n\n"
        f"Material:\n{state['research']}\n\nObservações do crítico:\n{state['critique']}"
    )
    return {"report": llm.complete(prompt, system="Você é um escritor técnico em português.").text}


def should_iterate(state: State) -> str:
    if state["critique"].strip().upper().startswith("OK") or state["iterations"] >= 1:
        return "writer"
    return "researcher"


def increment(state: State) -> dict:
    return {"iterations": state["iterations"] + 1}


def build_graph():
    g = StateGraph(State)
    g.add_node("researcher", researcher)
    g.add_node("critic", critic)
    g.add_node("inc", increment)
    g.add_node("writer", writer)
    g.add_edge(START, "researcher")
    g.add_edge("researcher", "critic")
    g.add_edge("critic", "inc")
    g.add_conditional_edges("inc", should_iterate, {"researcher": "researcher", "writer": "writer"})
    g.add_edge("writer", END)
    return g.compile()


@app.command()
def main(topico: str) -> None:
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    graph = build_graph()
    state = graph.invoke({"topic": topico, "research": "", "critique": "", "iterations": 0, "report": ""})
    (out_dir / "relatorio.md").write_text(state["report"], encoding="utf-8")
    typer.echo(f"Relatório salvo em out/relatorio.md ({len(state['report'])} chars)")


if __name__ == "__main__":
    app()
