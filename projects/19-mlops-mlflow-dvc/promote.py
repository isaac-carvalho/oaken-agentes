"""Promove a melhor versão do modelo registrado para 'Production' se passar do AUC mínimo."""
import mlflow
from mlflow.tracking import MlflowClient

MIN_AUC = 0.70
MODEL_NAME = "oaken-clf"


def main() -> None:
    client = MlflowClient()
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    if not versions:
        print(f"Nenhuma versão registrada para {MODEL_NAME}. Rode `dvc repro` primeiro.")
        return
    best = None
    for v in versions:
        run = mlflow.get_run(v.run_id)
        auc = run.data.metrics.get("auc_test", 0)
        if auc >= MIN_AUC and (best is None or auc > best[1]):
            best = (v, auc)
    if not best:
        print(f"Nenhuma versão atinge AUC >= {MIN_AUC}.")
        return
    v, auc = best
    client.transition_model_version_stage(name=MODEL_NAME, version=v.version, stage="Production", archive_existing_versions=True)
    print(f"Promovida versão {v.version} para Production (auc={auc:.3f})")


if __name__ == "__main__":
    main()
