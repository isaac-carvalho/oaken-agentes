"""Tests for project 19 — mlops-mlflow-dvc."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


# --------------- prepare: dataset generation ---------------

def test_prepare_generates_correct_columns():
    """Simulate prepare.py logic and check output."""
    rng = np.random.default_rng(42)
    n = 500
    df = pd.DataFrame({
        "x1": rng.normal(size=n),
        "x2": rng.normal(size=n),
        "x3": rng.uniform(0, 1, n),
    })
    noise = rng.normal(0, 0.5, n)
    logit = 0.7 * df["x1"] - 0.3 * df["x2"] + 0.5 * df["x3"] + noise
    df["y"] = (logit > 0).astype(int)
    assert set(df.columns) == {"x1", "x2", "x3", "y"}
    assert df["y"].nunique() == 2


def test_prepare_noise_prevents_perfect_auc():
    """With noise, AUC should be realistic (0.80-0.95), not 0.99+."""
    rng = np.random.default_rng(42)
    n = 3000
    df = pd.DataFrame({
        "x1": rng.normal(size=n),
        "x2": rng.normal(size=n),
        "x3": rng.uniform(0, 1, n),
    })
    noise = rng.normal(0, 0.5, n)
    logit = 0.7 * df["x1"] - 0.3 * df["x2"] + 0.5 * df["x3"] + noise
    df["y"] = (logit > 0).astype(int)

    X = df[["x1", "x2", "x3"]]
    y = df["y"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
    model = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=0)
    model.fit(X_tr, y_tr)
    auc = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])
    assert 0.80 <= auc <= 0.95, f"AUC {auc:.3f} outside expected range"


def test_prepare_deterministic():
    """Same seed should produce same data."""
    def gen(seed):
        rng = np.random.default_rng(seed)
        n = 100
        df = pd.DataFrame({"x1": rng.normal(size=n), "x2": rng.normal(size=n), "x3": rng.uniform(0, 1, n)})
        noise = rng.normal(0, 0.5, n)
        df["y"] = ((0.7 * df["x1"] - 0.3 * df["x2"] + 0.5 * df["x3"] + noise) > 0).astype(int)
        return df
    pd.testing.assert_frame_equal(gen(7), gen(7))


# --------------- promote.py ---------------

def test_promote_no_versions():
    """Should print message when no versions exist."""
    from promote import main, MODEL_NAME
    mock_client = MagicMock()
    mock_client.search_model_versions.return_value = []

    with patch("promote.MlflowClient", return_value=mock_client), \
         patch("builtins.print") as mock_print:
        main()
        mock_print.assert_called_once()
        assert "Nenhuma versão" in mock_print.call_args[0][0]


def test_promote_below_threshold():
    """Should not promote if AUC < MIN_AUC."""
    from promote import main, MIN_AUC

    mock_version = MagicMock()
    mock_version.run_id = "run1"
    mock_version.version = "1"

    mock_run = MagicMock()
    mock_run.data.metrics = {"auc_test": 0.50}

    mock_client = MagicMock()
    mock_client.search_model_versions.return_value = [mock_version]

    with patch("promote.MlflowClient", return_value=mock_client), \
         patch("promote.mlflow") as mock_mlflow, \
         patch("builtins.print") as mock_print:
        mock_mlflow.get_run.return_value = mock_run
        main()
        assert "Nenhuma versão atinge" in mock_print.call_args[0][0]


def test_promote_selects_best():
    """Should promote the version with highest AUC."""
    from promote import main

    versions = []
    runs = {}
    for i, auc in enumerate([0.75, 0.85, 0.80], start=1):
        v = MagicMock()
        v.run_id = f"run{i}"
        v.version = str(i)
        versions.append(v)
        r = MagicMock()
        r.data.metrics = {"auc_test": auc}
        runs[f"run{i}"] = r

    mock_client = MagicMock()
    mock_client.search_model_versions.return_value = versions

    with patch("promote.MlflowClient", return_value=mock_client), \
         patch("promote.mlflow") as mock_mlflow, \
         patch("builtins.print"):
        mock_mlflow.get_run.side_effect = lambda rid: runs[rid]
        main()
        mock_client.transition_model_version_stage.assert_called_once()
        call_kwargs = mock_client.transition_model_version_stage.call_args
        assert call_kwargs[1]["version"] == "2"  # version with AUC 0.85
