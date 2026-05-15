"""Inferência sobre uma imagem usando o modelo TorchScript."""
from __future__ import annotations

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

import torch
import typer
from PIL import Image
from torchvision import transforms

app = typer.Typer()
OUT = Path(__file__).parent / "out"


@app.command()
def main(imagem: Path) -> None:
    if not (OUT / "model.pt").exists():
        raise typer.BadParameter("Rode train.py antes.")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    classes = json.loads((OUT / "classes.json").read_text())
    model = torch.jit.load(str(OUT / "model.pt"), map_location=device).eval().to(device)
    tfm = transforms.Compose([transforms.Resize((64, 64)), transforms.ToTensor()])
    x = tfm(Image.open(imagem).convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        probs = model(x).softmax(1)[0]
    top = torch.topk(probs, k=3)
    for p, idx in zip(top.values.tolist(), top.indices.tolist()):
        typer.echo(f"  {classes[idx]:12s} {p:.3f}")


if __name__ == "__main__":
    app()
