"""Agente HTTP minimalista para empacotamento."""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

# Self-contained: _shared está no mesmo diretório (cópia local para o container).
sys.path.insert(0, str(Path(__file__).parent))
from _shared import get_default_client  # noqa: E402

app = FastAPI(title="Oaken Agent", version="1.0.0")
_llm = get_default_client()


class Pergunta(BaseModel):
    prompt: str


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
    return {"status": "ready", "provider": _llm.provider}


@app.post("/chat")
def chat(p: Pergunta) -> dict[str, str]:
    resp = _llm.complete(p.prompt, system="Responda em português, objetivo.")
    return {"reply": resp.text, "provider": resp.provider, "model": resp.model}
