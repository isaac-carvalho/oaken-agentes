"""Indexa arquivos .txt/.md em ChromaDB."""
from __future__ import annotations

from pathlib import Path

import chromadb
import typer
from chromadb.utils import embedding_functions

CHROMA_DIR = Path(__file__).parent / "chroma"
COLLECTION = "kb"

app = typer.Typer()


@app.command()
def main(diretorio: Path) -> None:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
    coll = client.get_or_create_collection(COLLECTION, embedding_function=embedder)
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
