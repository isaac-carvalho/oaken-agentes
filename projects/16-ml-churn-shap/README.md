# 16 — Classificador de Churn + SHAP

> **Carreira Alura:** Engenharia de Agentes — Nível 2 (*Machine Learning*)

Pipeline completo de ML supervisionado: dataset sintético de telecom, **XGBoost** para prever churn, **SHAP** para interpretabilidade global e local, e dashboard **Streamlit** para explorar predições.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Modelo | `xgboost`, `scikit-learn` |
| Interpretabilidade | `shap` |
| Dashboard | `streamlit` |

## Como rodar

```bash
pip install -r requirements.txt
python train.py                     # gera modelo.pkl + métricas
streamlit run dashboard.py          # explora interpretabilidade
```

## Entregáveis para portfólio
- AUC, precision, recall, matriz de confusão
- Feature importance via SHAP (global + waterfall por amostra)
- Dashboard interativo com sliders de features
