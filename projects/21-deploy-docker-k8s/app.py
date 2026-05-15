"""Agente HTTP minimalista para empacotamento."""
from __future__ import annotations

import functools
import logging
import os
import secrets
import sys

log = logging.getLogger(__name__)
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

# Self-contained: _shared está no mesmo diretório (cópia local para o container).
sys.path.insert(0, str(Path(__file__).parent))
from _shared import apply_security, get_default_client  # noqa: E402

app = FastAPI(title="Oaken Agent", version="1.0.0")
apply_security(
    app,
    allow_origins=os.environ.get("OAKEN_ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_methods=["GET", "POST"],
    rate_limit_per_minute=int(os.environ.get("OAKEN_RATE_LIMIT", "60")),
)
_API_KEY = os.environ.get("OAKEN_API_KEY")


@functools.lru_cache(maxsize=1)
def _get_llm():
    return get_default_client()


if os.environ.get("OAKEN_ENV") == "production" and not _API_KEY:
    raise RuntimeError("OAKEN_API_KEY obrigatória em produção. Defina a variável de ambiente.")


def _check_api_key(x_api_key: str | None) -> None:
    """Exige API key se OAKEN_API_KEY estiver configurada."""
    if _API_KEY is None:
        return  # auth desabilitada (dev mode)
    if not x_api_key or not secrets.compare_digest(x_api_key, _API_KEY):
        raise HTTPException(401, "unauthorized")


class Pergunta(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


@app.get("/health")
def health() -> dict:
    """Health check that verifies core dependencies are importable."""
    checks: dict[str, str] = {}
    for mod_name in ("fastapi", "pydantic", "uvicorn"):
        try:
            __import__(mod_name)
            checks[mod_name] = "ok"
        except ImportError:
            checks[mod_name] = "missing"
    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ok" if all_ok else "degraded", "dependencies": checks}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "provider": _get_llm().provider}


@app.post("/chat")
def chat(p: Pergunta, x_api_key: str | None = Header(default=None)) -> dict[str, str]:
    _check_api_key(x_api_key)
    resp = _get_llm().complete(p.prompt, system="Responda em português, objetivo.")
    return {"reply": resp.text, "provider": resp.provider, "model": resp.model}
