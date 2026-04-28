"""Carregamento padronizado de variáveis de ambiente (.env)."""
from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv_simple(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_env(start: Path | None = None) -> None:
    """Carrega .env subindo do diretório atual até a raiz do repo."""
    cwd = (start or Path.cwd()).resolve()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".env"
        if candidate.exists():
            _load_dotenv_simple(candidate)
            return
        if (parent / ".git").exists():
            break


def get_env(key: str, default: str | None = None) -> str | None:
    load_env()
    return os.environ.get(key, default)


def require_env(key: str) -> str:
    value = get_env(key)
    if not value:
        raise RuntimeError(
            f"Variável de ambiente obrigatória ausente: {key}. "
            f"Defina no .env ou exporte no shell."
        )
    return value
