"""CLI conversacional usando o grafo."""
from __future__ import annotations

import logging

import typer

log = logging.getLogger(__name__)

from agent import build_graph

app = typer.Typer()


@app.command()
def main(session: str = "default") -> None:
    graph = build_graph()
    cfg = {"configurable": {"thread_id": session}}
    typer.echo("Pergunte (ctrl-d para sair):")
    while True:
        try:
            q = input("> ").strip()
        except EOFError:
            break
        if not q:
            continue
        out = graph.invoke({"question": q, "messages": []}, cfg)
        typer.echo(f"\n{out['final']}\n")


if __name__ == "__main__":
    app()
