"""Wrapper CLIP + ChromaDB para indexação e busca multimodal.

Tenta usar OpenCLIP (ViT-B/32 laion2b_s34b_b79k). Se HuggingFace estiver
inacessível, cai num backend "hash multimodal" que ainda demonstra o pipeline
ponta-a-ponta — não substitui CLIP de verdade.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

import chromadb
from PIL import Image

CHROMA_DIR = Path(__file__).parent / "chroma"
COLLECTION = "multimodal"
_DIM = 512


def _hash_text_to_vec(text: str, dim: int = _DIM) -> list[float]:
    v = [0.0] * dim
    for word in text.lower().split():
        idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % dim
        v[idx] += 1.0
    norm = sum(x * x for x in v) ** 0.5
    return [x / norm for x in v] if norm > 0 else v


def _hash_image_to_vec(path: Path, dim: int = _DIM) -> list[float]:
    """Embedding deterministico baseado em estatisticas de bloco da imagem.
    Resultado pobre semanticamente, mas garante pipeline funcional offline."""
    img = Image.open(path).convert("RGB").resize((32, 32))
    pixels = list(img.getdata())
    v = [0.0] * dim
    for i, (r, g, b) in enumerate(pixels):
        idx = (i * 7 + r * 3 + g * 5 + b * 2) % dim
        v[idx] += (r + g + b) / 765.0
    norm = sum(x * x for x in v) ** 0.5
    return [x / norm for x in v] if norm > 0 else v


class _OpenClipBackend:
    name = "open-clip ViT-B/32 laion2b_s34b_b79k"

    def __init__(self) -> None:
        import open_clip
        import torch

        self._torch = torch
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="laion2b_s34b_b79k"
        )
        self.tokenizer = open_clip.get_tokenizer("ViT-B-32")
        self.model = self.model.to(self._device).eval()

    def embed_image(self, path: Path) -> list[float]:
        img = self.preprocess(Image.open(path).convert("RGB")).unsqueeze(0).to(self._device)
        with self._torch.no_grad():
            feat = self.model.encode_image(img)
        feat = feat / feat.norm(dim=-1, keepdim=True)
        return feat[0].cpu().tolist()

    def embed_text(self, text: str) -> list[float]:
        tokens = self.tokenizer([text]).to(self._device)
        with self._torch.no_grad():
            feat = self.model.encode_text(tokens)
        feat = feat / feat.norm(dim=-1, keepdim=True)
        return feat[0].cpu().tolist()


class _HashBackend:
    name = "hash-multimodal-512 (offline fallback — qualidade limitada)"

    def embed_image(self, path: Path) -> list[float]:
        return _hash_image_to_vec(path)

    def embed_text(self, text: str) -> list[float]:
        return _hash_text_to_vec(text)


def _make_backend():
    try:
        return _OpenClipBackend()
    except Exception:
        return _HashBackend()


class ClipIndex:
    def __init__(self) -> None:
        self.backend = _make_backend()
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.coll = self.client.get_or_create_collection(COLLECTION)

    def embed_image(self, path: Path) -> list[float]:
        return self.backend.embed_image(path)

    def embed_text(self, text: str) -> list[float]:
        return self.backend.embed_text(text)

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
