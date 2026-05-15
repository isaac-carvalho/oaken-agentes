"""Indexa arquivos .txt/.md em ChromaDB."""
from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)

import chromadb
import typer

from embedder import get_embedder

CHROMA_DIR = Path(__file__).parent / "chroma"
COLLECTION = "knowledge"

app = typer.Typer()


@app.command()
def main(diretorio: Path) -> None:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    coll = client.get_or_create_collection(COLLECTION, embedding_function=get_embedder())
    n = 0
    for p in diretorio.iterdir():
        if p.suffix not in {".txt", ".md"}:
            continue
        text = p.read_text(encoding="utf-8")
        for i in range(0, len(text), 800):
            coll.upsert(documents=[text[i : i + 800]], ids=[f"{p.name}::{i}"], metadatas=[{"file": p.name}])
            n += 1
    typer.echo(f"{n} chunks indexados.")


if __name__ == "__main__":
    app()
