"""CLI helper que roteia tarefas para um provedor LLM."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import typer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

app = typer.Typer(help="Helper CLI multi-provider para tarefas com LLM.")

# --- Retry / backoff ---

MAX_RETRIES = 3
BASE_DELAY = 1.0  # seconds


class LLMRequestError(Exception):
    """Erro ao chamar o LLM após todas as tentativas."""


def _ask_with_retry(system: str, prompt: str, max_retries: int = MAX_RETRIES) -> str:
    """Chama o LLM com retry exponencial e contagem de tokens."""
    client = get_default_client()
    typer.echo(f"[provider={client.provider}]", err=True)

    last_exc: Exception | None = None
    for attempt in range(max_retries):
        try:
            resp = client.complete(prompt, system=system)
            # Log token usage when available
            if resp.usage:
                total = resp.usage.get("prompt", 0) + resp.usage.get("completion", 0)
                typer.echo(f"[tokens={total}]", err=True)
            return resp.text
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                delay = BASE_DELAY * (2 ** attempt)
                typer.echo(f"[retry {attempt + 1}/{max_retries} em {delay:.1f}s: {exc}]", err=True)
                time.sleep(delay)

    raise LLMRequestError(f"Falha após {max_retries} tentativas: {last_exc}")


def _ask(system: str, prompt: str) -> str:
    """Wrapper mantido para compatibilidade."""
    return _ask_with_retry(system, prompt)


def estimate_tokens(text: str) -> int:
    """Estimativa grosseira de tokens (~4 chars por token em português)."""
    return max(1, len(text) // 4)


@app.command()
def resumir(texto: str, max_palavras: int = typer.Option(80, help="Limite de palavras")) -> None:
    """Resume o texto em português."""
    if not texto.strip():
        typer.echo("Erro: texto vazio.", err=True)
        raise typer.Exit(code=1)
    system = f"Você é um resumidor preciso. Responda em até {max_palavras} palavras, em português."
    typer.echo(_ask(system, texto))


@app.command()
def traduzir(texto: str, idioma: str = typer.Option("inglês", help="Idioma destino")) -> None:
    """Traduz o texto para o idioma escolhido."""
    if not texto.strip():
        typer.echo("Erro: texto vazio.", err=True)
        raise typer.Exit(code=1)
    system = f"Você é um tradutor profissional. Traduza fielmente para {idioma}, sem comentários."
    typer.echo(_ask(system, texto))


@app.command()
def codigo(descricao: str, linguagem: str = typer.Option("python", help="Linguagem")) -> None:
    """Gera um trecho de código a partir da descrição."""
    if not descricao.strip():
        typer.echo("Erro: descrição vazia.", err=True)
        raise typer.Exit(code=1)
    system = (
        f"Você é um engenheiro de software. Gere código {linguagem} idiomático, "
        "comentado apenas onde necessário, dentro de um único bloco markdown."
    )
    typer.echo(_ask(system, descricao))


if __name__ == "__main__":
    app()
