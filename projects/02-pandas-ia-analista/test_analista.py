"""Testes unitários do EDA automático — rodam offline."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from main import _eda, _save_plots


# --- _eda ---

def _sample_df():
    return pd.DataFrame({
        "idade": [25, 30, 35, 40, None],
        "salario": [3000, 4000, 5000, 6000, 7000],
        "nome": ["Ana", "Bruno", "Carla", "Diego", "Eva"],
    })


def test_eda_basic_keys():
    df = _sample_df()
    info = _eda(df, target=None)
    assert "shape" in info
    assert "dtypes" in info
    assert "missing" in info
    assert "describe" in info
    assert info["shape"] == (5, 3)


def test_eda_missing_counts():
    df = _sample_df()
    info = _eda(df, target=None)
    assert info["missing"]["idade"] == 1
    assert info["missing"]["salario"] == 0


def test_eda_with_target_correlation():
    df = _sample_df()
    info = _eda(df, target="salario")
    assert "target_corr" in info
    assert "salario" in info["target_corr"]
    # Correlação de salário consigo mesmo == 1.0
    assert info["target_corr"]["salario"] == pytest.approx(1.0)


def test_eda_target_non_numeric_ignored():
    df = _sample_df()
    info = _eda(df, target="nome")
    assert "target_corr" not in info


def test_eda_target_missing_column():
    df = _sample_df()
    info = _eda(df, target="inexistente")
    assert "target_corr" not in info


def test_eda_empty_dataframe():
    df = pd.DataFrame({"a": pd.Series(dtype="float64")})
    info = _eda(df, target=None)
    assert info["shape"] == (0, 1)


# --- _save_plots ---

def test_save_plots_creates_files(tmp_path):
    df = _sample_df()
    paths = _save_plots(df, tmp_path / "plots")
    # Deve gerar histogramas para colunas numéricas (idade, salario)
    assert len(paths) == 2
    for p in paths:
        assert Path(p).exists()
        assert p.endswith(".png")


def test_save_plots_no_numeric(tmp_path):
    df = pd.DataFrame({"a": ["x", "y"], "b": ["w", "z"]})
    paths = _save_plots(df, tmp_path / "plots")
    assert paths == []
