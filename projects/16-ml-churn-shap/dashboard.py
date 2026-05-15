"""Dashboard de explicabilidade (Streamlit + SHAP)."""
from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)

import joblib
import pandas as pd
import shap
import streamlit as st

OUT = Path(__file__).parent / "out"

st.set_page_config(page_title="Churn + SHAP", layout="wide")
st.title("📉 Churn — Interpretabilidade com SHAP")

PROJECT_DIR = Path(__file__).resolve().parent


def _safe_path(p: Path) -> Path:
    """Valida que o path resolve dentro do diretório do projeto."""
    resolved = p.resolve()
    if not str(resolved).startswith(str(PROJECT_DIR)):
        raise ValueError(f"Path fora do diretório do projeto: {resolved}")
    return resolved


if not (OUT / "modelo.pkl").exists():
    st.warning("Rode `python train.py` primeiro para gerar o modelo.")
    st.stop()

model = joblib.load(_safe_path(OUT / "modelo.pkl"))
df = pd.read_csv(_safe_path(OUT / "dataset.csv"))
X = df.drop(columns=["churn"])

explainer = shap.TreeExplainer(model)

with st.sidebar:
    st.header("Cliente sintético")
    valores = {col: st.slider(col, float(X[col].min()), float(X[col].max()), float(X[col].mean())) for col in X.columns}

amostra = pd.DataFrame([valores])
proba = model.predict_proba(amostra)[0, 1]
st.metric("Probabilidade de churn", f"{proba:.0%}")

shap_values = explainer.shap_values(amostra)
st.subheader("Por que esse cliente?")
st.bar_chart(pd.Series(shap_values[0], index=X.columns).sort_values(key=abs))

st.subheader("Importância global (média absoluta)")
global_shap = explainer.shap_values(X.sample(500, random_state=0))
st.bar_chart(pd.Series(abs(global_shap).mean(0), index=X.columns).sort_values(ascending=False))
