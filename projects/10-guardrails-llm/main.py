"""Demo dos guardrails."""
from __future__ import annotations

import sys
from pathlib import Path

import typer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

from guardrails import safe_call

app = typer.Typer()


@app.command()
def main(prompt: str) -> None:
    client = get_default_client()
    result = safe_call(client, prompt)
    typer.echo(f"Redactions aplicadas: {result.redactions or 'nenhuma'}")
    if result.blocked:
        typer.echo(f"❌ BLOQUEADO: {result.reason}")
    else:
        typer.echo(f"✅ Resposta:\n{result.text}")


if __name__ == "__main__":
    app()
