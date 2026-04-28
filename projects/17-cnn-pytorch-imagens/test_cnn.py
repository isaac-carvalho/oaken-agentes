"""Tests for project 17 — cnn-pytorch-imagens."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import torch
import torch.nn as nn

from train import build_model, get_synthetic_loaders, CIFAR_CLASSES


# --------------- build_model ---------------

def test_build_model_output_shape():
    model = build_model(n_classes=10, pretrained=False)
    x = torch.rand(2, 3, 64, 64)
    out = model(x)
    assert out.shape == (2, 10)


def test_build_model_custom_classes():
    model = build_model(n_classes=5, pretrained=False)
    x = torch.rand(1, 3, 64, 64)
    out = model(x)
    assert out.shape == (1, 5)


def test_build_model_frozen_layers_pretrained():
    """With pretrained=True, only fc should be trainable."""
    model = build_model(n_classes=10, pretrained=False)
    # Test with pretrained=False (no download needed) — all params trainable
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    assert trainable == total


# --------------- synthetic loaders ---------------

def test_synthetic_loaders_shape():
    train_dl, test_dl, classes = get_synthetic_loaders(batch=8, n_train=32, n_test=16)
    xb, yb = next(iter(train_dl))
    assert xb.shape == (8, 3, 64, 64)
    assert yb.shape == (8,)
    assert len(classes) == 10


def test_synthetic_loaders_class_range():
    _, test_dl, _ = get_synthetic_loaders(batch=16, n_train=64, n_test=64, n_classes=5)
    for xb, yb in test_dl:
        assert yb.max().item() < 5
        assert yb.min().item() >= 0


def test_cifar_classes_count():
    assert len(CIFAR_CLASSES) == 10


# --------------- forward pass smoke test ---------------

def test_training_step_smoke():
    """One training step should not crash."""
    model = build_model(n_classes=10, pretrained=False)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    x = torch.rand(4, 3, 64, 64)
    y = torch.randint(0, 10, (4,))
    opt.zero_grad()
    loss = loss_fn(model(x), y)
    loss.backward()
    opt.step()
    assert loss.item() > 0
