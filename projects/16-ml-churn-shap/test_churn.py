"""Tests for project 16 — ml-churn-shap."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from train import synth_dataset


# --------------- synth_dataset ---------------

def test_synth_dataset_shape():
    df = synth_dataset(n=100, seed=0)
    assert df.shape == (100, 7)
    assert "churn" in df.columns


def test_synth_dataset_deterministic():
    df1 = synth_dataset(n=50, seed=7)
    df2 = synth_dataset(n=50, seed=7)
    pd.testing.assert_frame_equal(df1, df2)


def test_synth_dataset_churn_balance():
    """Churn should not be all 0 or all 1."""
    df = synth_dataset(n=2000, seed=42)
    ratio = df["churn"].mean()
    assert 0.05 < ratio < 0.95, f"Churn ratio {ratio} is too extreme"


def test_synth_dataset_value_ranges():
    df = synth_dataset(n=1000, seed=42)
    assert df["valor_mensal"].min() >= 20
    assert df["valor_mensal"].max() <= 200
    assert df["uso_dados_gb"].min() >= 0.1
    assert df["uso_dados_gb"].max() <= 60
    assert df["tempo_meses"].min() >= 1
    assert df["tempo_meses"].max() <= 71


def test_synth_dataset_columns():
    df = synth_dataset(n=10)
    expected = {"tempo_meses", "valor_mensal", "uso_dados_gb",
                "atendimentos_30d", "fidelidade_score", "atraso_pagamento", "churn"}
    assert set(df.columns) == expected


# --------------- train pipeline (mocked output) ---------------

def test_train_produces_reasonable_auc():
    """Full train pipeline should yield AUC > 0.7 on synthetic data."""
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split
    from xgboost import XGBClassifier

    df = synth_dataset(n=2000, seed=99)
    X = df.drop(columns=["churn"])
    y = df["churn"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
    model = XGBClassifier(n_estimators=50, max_depth=3, eval_metric="auc")
    model.fit(X_tr, y_tr)
    auc = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])
    assert auc > 0.7, f"AUC too low: {auc}"
