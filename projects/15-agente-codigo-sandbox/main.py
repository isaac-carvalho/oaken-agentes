"""Loop write → run → fix."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import typer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

from sandbox import run_in_docker

app = typer.Typer()
CODE_BLOCK = re.compile(r"```(?:python)?\s*(.+?)```", re.DOTALL)


def extract_code(text: str) -> str:
    m = CODE_BLOCK.search(text)
    return m.group(1).strip() if m else text.strip()


@app.command()
def main(tarefa: str, max_iter: int = 5) -> None:
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    llm = get_default_client()
    history = ""
    for it in range(1, max_iter + 1):
        prompt = (
            f"Tarefa: {tarefa}\n\n{history}\n"
            "Escreva o código Python completo num único bloco ```python ...```. "
            "Inclua os testes assert; o script deve imprimir 'OK' ao final se tudo passar."
        )
        resp = llm.complete(prompt, system="Você é um engenheiro Python sênior.").text
        code = extract_code(resp)
        (out_dir / f"iter{it}.py").write_text(code, encoding="utf-8")
        ok, output = run_in_docker(code)
        typer.echo(f"\n--- iter {it} (ok={ok}) ---\n{output[:600]}\n")
        if ok and "OK" in output:
            typer.echo("✅ Sucesso.")
            return
        history += f"\nTentativa {it} falhou. Output:\n{output}\nCorrija o código."
    typer.echo("❌ Não convergiu.")


if __name__ == "__main__":
    app()
