"""Treino com transfer learning ResNet18 em CIFAR-10."""
from __future__ import annotations

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

import torch
import torch.nn as nn
import typer
from torch.utils.data import DataLoader, TensorDataset
from torchvision import datasets, models, transforms

app = typer.Typer()
OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

CIFAR_CLASSES = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck",
]


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


def get_synthetic_loaders(batch: int, n_train: int = 512, n_test: int = 128, n_classes: int = 10):
    """Dataset sinteico para smoke test offline."""
    g = torch.Generator().manual_seed(0)
    Xtr = torch.rand(n_train, 3, 64, 64, generator=g)
    ytr = torch.randint(0, n_classes, (n_train,), generator=g)
    Xte = torch.rand(n_test, 3, 64, 64, generator=g)
    yte = torch.randint(0, n_classes, (n_test,), generator=g)
    return (
        DataLoader(TensorDataset(Xtr, ytr), batch_size=batch, shuffle=True),
        DataLoader(TensorDataset(Xte, yte), batch_size=batch),
        CIFAR_CLASSES[:n_classes],
    )


def build_model(n_classes: int, pretrained: bool = True) -> nn.Module:
    weights = "IMAGENET1K_V1" if pretrained else None
    model = models.resnet18(weights=weights)
    if pretrained:
        for p in model.parameters():
            p.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, n_classes)
    return model


@app.command()
def main(
    epochs: int = 3,
    batch: int = 64,
    lr: float = 1e-3,
    no_download: bool = typer.Option(False, "--no-download", help="Usa dataset sintético (sem CIFAR-10)"),
    no_pretrained: bool = typer.Option(False, "--no-pretrained", help="Sem pesos ImageNet (treina do zero)"),
) -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if no_download:
        typer.echo("[modo] dataset SINTÉTICO (smoke test)")
        train_loader, test_loader, classes = get_synthetic_loaders(batch)
    else:
        train_loader, test_loader, classes = get_loaders(batch)
    model = build_model(len(classes), pretrained=not no_pretrained).to(device)
    opt = torch.optim.Adam(
        model.fc.parameters() if not no_pretrained else model.parameters(),
        lr=lr,
    )
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
    torch.jit.trace(model.cpu(), torch.randn(1, 3, 64, 64)).save(str(OUT / "model.pt"))
    (OUT / "classes.json").write_text(json.dumps(classes))
    (OUT / "history.json").write_text(json.dumps(history, indent=2))
    typer.echo(f"Modelo salvo em {OUT / 'model.pt'}")


if __name__ == "__main__":
    app()
