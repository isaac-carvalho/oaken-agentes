"""EDA automática com narrativa gerada por LLM."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)

import pandas as pd
import typer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

app = typer.Typer()


def _eda(df: pd.DataFrame, target: str | None) -> dict:
    info = {
        "shape": df.shape,
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isna().sum().to_dict(),
        "describe": df.describe(include="all").to_dict(),
    }
    if target and target in df.columns and pd.api.types.is_numeric_dtype(df[target]):
        info["target_corr"] = df.corr(numeric_only=True)[target].to_dict()
    return info


def _save_plots(df: pd.DataFrame, out: Path) -> list[str]:
    import matplotlib.pyplot as plt

    out.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    for col in df.select_dtypes(include="number").columns[:6]:
        fig, ax = plt.subplots()
        df[col].hist(ax=ax, bins=30)
        ax.set_title(f"Histograma — {col}")
        path = out / f"hist_{col}.png"
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        paths.append(str(path))
    return paths


@app.command()
def main(
    csv: Path = typer.Argument(..., help="Caminho do CSV"),
    target: str = typer.Option(None, help="Coluna alvo para correlação"),
    out: Path = typer.Option(Path("out"), help="Diretório de saída"),
) -> None:
    df = pd.read_csv(csv)
    typer.echo(f"Carregado: {df.shape[0]} linhas × {df.shape[1]} colunas")

    summary = _eda(df, target)
    plots = _save_plots(df, out)

    client = get_default_client()
    summary_str = str(summary)[:3000]
    prompt = (
        "Você é um analista de dados sênior. Com base no resumo abaixo, "
        "produza um relatório em markdown com:\n"
        "1. Visão geral do dataset\n2. 5 insights numéricos\n3. Riscos de qualidade\n4. Próximos passos\n\n"
        f"Resumo:\n{summary_str}"
    )
    relatorio = client.complete(prompt, system="Resposta em português, objetiva.").text

    out.mkdir(parents=True, exist_ok=True)
    (out / "relatorio.md").write_text(relatorio, encoding="utf-8")
    typer.echo(f"Relatório salvo em {out / 'relatorio.md'}")
    typer.echo(f"Gráficos: {len(plots)} arquivos em {out}/")


if __name__ == "__main__":
    app()
