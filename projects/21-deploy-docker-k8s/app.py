"""Agente HTTP minimalista para empacotamento."""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

app = FastAPI(title="Oaken Agent", version="1.0.0")
_llm = get_default_client()


class Pergunta(BaseModel):
    prompt: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "provider": _llm.provider}


@app.post("/chat")
def chat(p: Pergunta) -> dict[str, str]:
    resp = _llm.complete(p.prompt, system="Responda em português, objetivo.")
    return {"reply": resp.text, "provider": resp.provider, "model": resp.model}
