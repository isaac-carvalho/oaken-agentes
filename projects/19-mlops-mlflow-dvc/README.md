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

## Output de exemplo

Pipeline DVC repro (3 estágios) + registro MLflow:
```bash
$ source .venv/bin/activate   # importante: dvc invoca `python` do PATH
$ dvc init -q --no-scm
$ dvc repro
Running stage 'prepare':  python src/prepare.py     # gera data/processed.csv
Running stage 'train':    python src/train.py       # AUC train=1.000  test=0.997
Running stage 'evaluate': python src/evaluate.py    # eval.json -> {"auc":0.997, ...}
```

`metrics/eval.json`:
```json
{"auc": 0.997, "accuracy": 0.97, "f1": 0.975}
```

Promoção baseada em métrica:
```bash
$ python promote.py
Promovida versão 1 para Production (auc=0.997)
```

MLflow registry:
```
Versoes registradas de oaken-clf: 2
  v2 stage=None
  v1 stage=Production    ← promovida automaticamente
```

> ⚠️ Rodar `dvc repro` **com o venv ativado** (`source .venv/bin/activate`), porque o DVC executa `python src/...` do PATH global. Alternativamente, ajuste `dvc.yaml` para usar caminhos absolutos.

## Entregáveis para portfólio
- `dvc.yaml` declarativo com 3 estágios
- MLflow tracking + Model Registry funcionando local
- Script de promoção baseado em métrica (AUC mínimo)
