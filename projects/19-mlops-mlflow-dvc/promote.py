"""Promove a melhor versão do modelo registrado para 'Production' se passar do AUC mínimo."""
import logging
import os

os.environ.setdefault("MLFLOW_HTTP_REQUEST_TIMEOUT", "30")

import mlflow
from mlflow.tracking import MlflowClient

log = logging.getLogger(__name__)

MIN_AUC = 0.70
MODEL_NAME = "oaken-clf"


def main() -> None:
    client = MlflowClient()
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    if not versions:
        log.info("Nenhuma versão registrada para %s. Rode `dvc repro` primeiro.", MODEL_NAME)
        return
    best = None
    for v in versions:
        run = mlflow.get_run(v.run_id)
        auc = run.data.metrics.get("auc_test", 0)
        if auc >= MIN_AUC and (best is None or auc > best[1]):
            best = (v, auc)
    if not best:
        log.info("Nenhuma versão atinge AUC >= %s.", MIN_AUC)
        return
    v, auc = best
    try:
        client.set_registered_model_alias(MODEL_NAME, "production", v.version)
        log.info("Promovida versão %s para Production via alias (auc=%.3f)", v.version, auc)
    except (AttributeError, Exception):
        client.transition_model_version_stage(name=MODEL_NAME, version=v.version, stage="Production", archive_existing_versions=True)
        log.info("Promovida versão %s para Production via stage (auc=%.3f)", v.version, auc)


if __name__ == "__main__":
    main()
