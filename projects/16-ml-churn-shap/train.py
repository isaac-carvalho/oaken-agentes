"""Treina XGBoost para churn em dataset sintético."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)


def synth_dataset(n: int = 4000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "tempo_meses": rng.integers(1, 72, n),
        "valor_mensal": rng.normal(80, 25, n).clip(20, 200),
        "uso_dados_gb": rng.normal(15, 8, n).clip(0.1, 60),
        "atendimentos_30d": rng.poisson(0.5, n),
        "fidelidade_score": rng.uniform(0, 1, n),
        "atraso_pagamento": rng.binomial(1, 0.15, n),
    })
    logit = (
        -1.5
        + 0.04 * (60 - df["tempo_meses"])
        + 0.02 * (df["valor_mensal"] - 80)
        - 1.8 * df["fidelidade_score"]
        + 1.0 * df["atraso_pagamento"]
        + 0.6 * df["atendimentos_30d"]
    )
    p = 1 / (1 + np.exp(-logit))
    df["churn"] = (rng.uniform(size=n) < p).astype(int)
    return df


def main() -> None:
    df = synth_dataset()
    X = df.drop(columns=["churn"])
    y = df["churn"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)

    model = XGBClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.1,
        eval_metric="auc", n_jobs=-1, tree_method="hist",
    )
    model.fit(X_tr, y_tr)

    proba = model.predict_proba(X_te)[:, 1]
    pred = (proba >= 0.5).astype(int)
    metrics = {
        "auc": float(roc_auc_score(y_te, proba)),
        "report": classification_report(y_te, pred, output_dict=True),
        "n_train": len(X_tr),
        "n_test": len(X_te),
    }
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
    joblib.dump(model, OUT / "modelo.pkl")
    df.to_csv(OUT / "dataset.csv", index=False)
    print(f"AUC={metrics['auc']:.3f}  artefatos em {OUT}/")


if __name__ == "__main__":
    main()
