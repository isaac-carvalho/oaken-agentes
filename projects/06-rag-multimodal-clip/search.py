"""Busca cross-modal: query por texto OU imagem."""
from __future__ import annotations

from pathlib import Path

import typer

from clip_index import ClipIndex

app = typer.Typer()


@app.command()
def main(
    texto: str = typer.Option(None, help="Query textual"),
    imagem: Path = typer.Option(None, help="Query por imagem"),
    k: int = 5,
) -> None:
    if not texto and not imagem:
        raise typer.BadParameter("Informe --texto ou --imagem")
    idx = ClipIndex()
    if imagem:
        emb = idx.embed_image(imagem)
        typer.echo(f"Query: imagem {imagem}")
    else:
        emb = idx.embed_text(texto)
        typer.echo(f"Query: texto '{texto}'")
    for hit in idx.search(emb, k=k):
        typer.echo(f"  [{hit['distance']:.3f}] {hit['meta']['modality']:5s} {hit['meta']['file']}  — {hit['meta']['caption'][:80]}")


if __name__ == "__main__":
    app()
