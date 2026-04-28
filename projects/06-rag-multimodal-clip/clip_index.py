"""Wrapper CLIP + ChromaDB para indexação e busca multimodal."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import chromadb
import open_clip
import torch
from PIL import Image

CHROMA_DIR = Path(__file__).parent / "chroma"
COLLECTION = "multimodal"
_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class ClipIndex:
    def __init__(self) -> None:
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="laion2b_s34b_b79k"
        )
        self.tokenizer = open_clip.get_tokenizer("ViT-B-32")
        self.model = self.model.to(_DEVICE).eval()
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.coll = self.client.get_or_create_collection(COLLECTION)

    def embed_image(self, path: Path) -> list[float]:
        img = self.preprocess(Image.open(path).convert("RGB")).unsqueeze(0).to(_DEVICE)
        with torch.no_grad():
            feat = self.model.encode_image(img)
        feat = feat / feat.norm(dim=-1, keepdim=True)
        return feat[0].cpu().tolist()

    def embed_text(self, text: str) -> list[float]:
        tokens = self.tokenizer([text]).to(_DEVICE)
        with torch.no_grad():
            feat = self.model.encode_text(tokens)
        feat = feat / feat.norm(dim=-1, keepdim=True)
        return feat[0].cpu().tolist()

    def add_image(self, path: Path, caption: str | None = None) -> None:
        emb = self.embed_image(path)
        self.coll.upsert(
            ids=[str(path)],
            embeddings=[emb],
            metadatas=[{"file": str(path), "modality": "image", "caption": caption or ""}],
            documents=[caption or path.name],
        )

    def add_text(self, doc_id: str, text: str) -> None:
        emb = self.embed_text(text)
        self.coll.upsert(
            ids=[doc_id],
            embeddings=[emb],
            metadatas=[{"file": doc_id, "modality": "text", "caption": text[:120]}],
            documents=[text],
        )

    def search(self, query_emb: Iterable[float], k: int = 5) -> list[dict]:
        res = self.coll.query(query_embeddings=[list(query_emb)], n_results=k)
        out = []
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            out.append({"doc": doc, "meta": meta, "distance": dist})
        return out
