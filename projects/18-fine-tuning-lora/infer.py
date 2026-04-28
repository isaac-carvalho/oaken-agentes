"""Inferência usando o adapter LoRA treinado."""
from __future__ import annotations

from pathlib import Path

import typer

app = typer.Typer()
ADAPTER = Path(__file__).parent / "out" / "adapter"


@app.command()
def main(prompt: str, base: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0", max_new: int = 200) -> None:
    if not ADAPTER.exists():
        raise typer.BadParameter("Treine antes (python train.py).")
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(str(ADAPTER))
    model = AutoModelForCausalLM.from_pretrained(base, torch_dtype=torch.float16, device_map="auto")
    model = PeftModel.from_pretrained(model, str(ADAPTER))
    text = f"### Instrução:\n{prompt}\n\n### Resposta:\n"
    inputs = tok(text, return_tensors="pt").to(model.device)
    out = model.generate(**inputs, max_new_tokens=max_new, do_sample=False)
    typer.echo(tok.decode(out[0], skip_special_tokens=True))


if __name__ == "__main__":
    app()
