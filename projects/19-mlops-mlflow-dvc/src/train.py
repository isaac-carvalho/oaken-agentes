"""Treina + registra no MLflow."""
import json
import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)

os.environ.setdefault("MLFLOW_HTTP_REQUEST_TIMEOUT", "30")

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

_ROOT = Path(__file__).resolve().parent.parent
DATA = _ROOT / "data" / "processed.csv"
MODELS = _ROOT / "models"
METRICS = _ROOT / "metrics"
MODELS.mkdir(exist_ok=True)
METRICS.mkdir(exist_ok=True)

mlflow.set_experiment("oaken-19-mlops")

df = pd.read_csv(DATA)
X = df[["x1", "x2", "x3"]]
y = df["y"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)

with mlflow.start_run() as run:
    params = {"n_estimators": 200, "max_depth": 6}
    model = RandomForestClassifier(**params, random_state=0)
    model.fit(X_tr, y_tr)
    auc_tr = roc_auc_score(y_tr, model.predict_proba(X_tr)[:, 1])
    auc_te = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])

    mlflow.log_params(params)
    mlflow.log_metrics({"auc_train": auc_tr, "auc_test": auc_te})
    mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name="oaken-clf")

    joblib.dump(model, MODELS / "model.pkl")
    (METRICS / "train.json").write_text(json.dumps({"auc_train": auc_tr, "auc_test": auc_te, "run_id": run.info.run_id}, indent=2))

log.info("training_complete", extra={"auc_train": f"{auc_tr:.3f}", "auc_test": f"{auc_te:.3f}"})
