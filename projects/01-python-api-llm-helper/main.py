"""CLI helper que roteia tarefas para um provedor LLM."""
from __future__ import annotations

import sys
from pathlib import Path

import typer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

app = typer.Typer(help="Helper CLI multi-provider para tarefas com LLM.")


def _ask(system: str, prompt: str) -> str:
    client = get_default_client()
    typer.echo(f"[provider={client.provider}]", err=True)
    return client.complete(prompt, system=system).text


@app.command()
def resumir(texto: str, max_palavras: int = typer.Option(80, help="Limite de palavras")) -> None:
    """Resume o texto em português."""
    system = f"Você é um resumidor preciso. Responda em até {max_palavras} palavras, em português."
    typer.echo(_ask(system, texto))


@app.command()
def traduzir(texto: str, idioma: str = typer.Option("inglês", help="Idioma destino")) -> None:
    """Traduz o texto para o idioma escolhido."""
    system = f"Você é um tradutor profissional. Traduza fielmente para {idioma}, sem comentários."
    typer.echo(_ask(system, texto))


@app.command()
def codigo(descricao: str, linguagem: str = typer.Option("python", help="Linguagem")) -> None:
    """Gera um trecho de código a partir da descrição."""
    system = (
        f"Você é um engenheiro de software. Gere código {linguagem} idiomático, "
        "comentado apenas onde necessário, dentro de um único bloco markdown."
    )
    typer.echo(_ask(system, descricao))


if __name__ == "__main__":
    app()
