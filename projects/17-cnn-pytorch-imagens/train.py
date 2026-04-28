"""Treino com transfer learning ResNet18 em CIFAR-10."""
from __future__ import annotations

import json
from pathlib import Path

import torch
import torch.nn as nn
import typer
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

app = typer.Typer()
OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)


def get_loaders(batch: int):
    tfm_train = transforms.Compose([
        transforms.Resize(64),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])
    tfm_test = transforms.Compose([transforms.Resize(64), transforms.ToTensor()])
    train = datasets.CIFAR10(OUT / "data", train=True, download=True, transform=tfm_train)
    test = datasets.CIFAR10(OUT / "data", train=False, download=True, transform=tfm_test)
    return (
        DataLoader(train, batch_size=batch, shuffle=True, num_workers=2),
        DataLoader(test, batch_size=batch, num_workers=2),
        train.classes,
    )


def build_model(n_classes: int) -> nn.Module:
    model = models.resnet18(weights="IMAGENET1K_V1")
    for p in model.parameters():
        p.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, n_classes)
    return model


@app.command()
def main(epochs: int = 3, batch: int = 64, lr: float = 1e-3) -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_loader, test_loader, classes = get_loaders(batch)
    model = build_model(len(classes)).to(device)
    opt = torch.optim.Adam(model.fc.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    history = []
    for ep in range(1, epochs + 1):
        model.train()
        run_loss = 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            run_loss += loss.item()
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for xb, yb in test_loader:
                xb, yb = xb.to(device), yb.to(device)
                correct += (model(xb).argmax(1) == yb).sum().item()
                total += yb.size(0)
        acc = correct / total
        history.append({"epoch": ep, "loss": run_loss / len(train_loader), "val_acc": acc})
        typer.echo(f"epoch {ep} loss={history[-1]['loss']:.4f} val_acc={acc:.3f}")
    torch.jit.script(model.cpu()).save(str(OUT / "model.pt"))
    (OUT / "classes.json").write_text(json.dumps(classes))
    (OUT / "history.json").write_text(json.dumps(history, indent=2))
    typer.echo(f"Modelo salvo em {OUT / 'model.pt'}")


if __name__ == "__main__":
    app()
