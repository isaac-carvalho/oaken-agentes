# 19 — Pipeline MLOps com MLflow + DVC

> **Carreira Alura:** Engenharia de Agentes — Nível 3 (*MLOps*)

Pipeline reproduzível: **DVC** versiona dados e estágios de processamento; **MLflow** registra experimentos, métricas e o **Model Registry**. Inclui demo de promoção `Staging → Production`.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Versionamento de dados | DVC |
| Tracking + Registry | MLflow |
| Modelo | scikit-learn (LogReg/RandomForest) |

## Como rodar

```bash
pip install -r requirements.txt
dvc init -q --no-scm        # primeira vez (sem git auto-config)
dvc repro                    # roda o pipeline (prepare → train → evaluate)
mlflow ui --port 5000        # inspecione experimentos
python promote.py            # promove melhor modelo para Production
```

## Entregáveis para portfólio
- `dvc.yaml` declarativo com 3 estágios
- MLflow tracking + Model Registry funcionando local
- Script de promoção baseado em métrica (AUC mínimo)
