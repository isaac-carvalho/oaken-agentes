"""Tests for project 18 — fine-tuning-lora."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from train import format_example


# --------------- format_example ---------------

def test_format_example_basic():
    rec = {"instruction": "Explique IA", "response": "IA eh inteligencia artificial."}
    result = format_example(rec)
    assert "### Instrução:" in result
    assert "Explique IA" in result
    assert "### Resposta:" in result
    assert "IA eh inteligencia artificial." in result


def test_format_example_empty_fields():
    rec = {"instruction": "", "response": ""}
    result = format_example(rec)
    assert "### Instrução:\n" in result
    assert "### Resposta:\n" in result


def test_format_example_special_chars():
    rec = {"instruction": "O que é 2+2?", "response": "É 4! (ou ~4)"}
    result = format_example(rec)
    assert "2+2?" in result
    assert "(ou ~4)" in result


# --------------- dry-run mode (no GPU) ---------------

def test_train_dry_run(tmp_path):
    """Without CUDA, train.py should create DRY_RUN.txt."""
    import train

    original_out = train.OUT
    train.OUT = tmp_path / "out"

    with patch("torch.cuda.is_available", return_value=False):
        from typer.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(train.app, [])

    assert (tmp_path / "out" / "DRY_RUN.txt").exists()
    content = (tmp_path / "out" / "DRY_RUN.txt").read_text()
    assert "base=" in content
    assert "epochs=" in content

    train.OUT = original_out


# --------------- infer module existence ---------------

def test_infer_adapter_check():
    """infer.main should raise if adapter dir doesn't exist."""
    import infer

    with patch.object(Path, "exists", return_value=False):
        from typer.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(infer.app, ["test prompt"])
        assert result.exit_code != 0


# --------------- format roundtrip ---------------

def test_format_example_structure():
    rec = {"instruction": "hello", "response": "world"}
    text = format_example(rec)
    lines = text.split("\n")
    assert lines[0] == "### Instrução:"
    assert lines[1] == "hello"
    assert lines[3] == "### Resposta:"
    assert lines[4] == "world"
