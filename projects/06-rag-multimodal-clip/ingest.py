"""Indexa imagens (.jpg/.png) e textos (.txt) de um diretório."""
from __future__ import annotations

from pathlib import Path

import typer

from clip_index import ClipIndex

app = typer.Typer()


@app.command()
def main(diretorio: Path) -> None:
    idx = ClipIndex()
    n_img = 0
    n_txt = 0
    for p in diretorio.iterdir():
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            idx.add_image(p)
            n_img += 1
        elif p.suffix.lower() == ".txt":
            idx.add_text(str(p), p.read_text(encoding="utf-8"))
            n_txt += 1
    typer.echo(f"Indexadas {n_img} imagens e {n_txt} textos.")


if __name__ == "__main__":
    app()
