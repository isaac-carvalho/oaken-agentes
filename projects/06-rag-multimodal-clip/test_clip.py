"""Testes unitários do CLIP index — rodam offline com HashBackend."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Mock chromadb antes de importar clip_index
sys.modules.setdefault("chromadb", MagicMock())

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from clip_index import _hash_text_to_vec, _hash_image_to_vec, _HashBackend, _DIM


# --- _hash_text_to_vec ---

def test_hash_text_basic():
    vec = _hash_text_to_vec("hello world")
    assert len(vec) == _DIM


def test_hash_text_normalized():
    vec = _hash_text_to_vec("texto de teste")
    norm = sum(x * x for x in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-6


def test_hash_text_empty():
    vec = _hash_text_to_vec("")
    assert all(x == 0.0 for x in vec)


def test_hash_text_deterministic():
    v1 = _hash_text_to_vec("repetido")
    v2 = _hash_text_to_vec("repetido")
    assert v1 == v2


def test_hash_text_different_inputs_differ():
    v1 = _hash_text_to_vec("gato")
    v2 = _hash_text_to_vec("cachorro")
    assert v1 != v2


# --- _hash_image_to_vec ---

def test_hash_image_to_vec(tmp_path):
    from PIL import Image
    img = Image.new("RGB", (64, 64), color=(128, 64, 32))
    path = tmp_path / "test.png"
    img.save(path)
    vec = _hash_image_to_vec(path)
    assert len(vec) == _DIM


def test_hash_image_normalized(tmp_path):
    from PIL import Image
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    path = tmp_path / "red.png"
    img.save(path)
    vec = _hash_image_to_vec(path)
    norm = sum(x * x for x in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-6


def test_hash_image_deterministic(tmp_path):
    from PIL import Image
    img = Image.new("RGB", (10, 10), color=(0, 255, 0))
    path = tmp_path / "green.png"
    img.save(path)
    v1 = _hash_image_to_vec(path)
    v2 = _hash_image_to_vec(path)
    assert v1 == v2


# --- _HashBackend ---

def test_hash_backend_text():
    b = _HashBackend()
    vec = b.embed_text("query")
    assert len(vec) == _DIM


def test_hash_backend_image(tmp_path):
    from PIL import Image
    img = Image.new("RGB", (20, 20), color=(100, 100, 100))
    path = tmp_path / "gray.png"
    img.save(path)
    b = _HashBackend()
    vec = b.embed_image(path)
    assert len(vec) == _DIM
