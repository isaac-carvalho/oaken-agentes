"""API de atendimento que classifica intenção e gera resposta."""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import apply_security, get_default_client  # noqa: E402

app = FastAPI(title="Atendimento WhatsApp")
apply_security(
    app,
    allow_origins=["http://localhost:5678"],  # n8n local default
    allow_methods=["GET", "POST"],
    rate_limit_per_minute=60,
)
_llm = get_default_client()

INTENCOES = ("saudacao", "duvida", "reclamacao", "outro")

PROMPT_INTENT = (
    "Classifique a mensagem em UMA das categorias: saudacao, duvida, reclamacao, outro. "
    "Devolva APENAS a palavra."
)
PROMPT_RESP = (
    "Você é um atendente educado e objetivo de uma loja online. "
    "Responda em português, em até 3 frases. Confirme que vai ajudar."
)


class Mensagem(BaseModel):
    telefone: str = Field(min_length=8, max_length=20)
    mensagem: str = Field(min_length=1, max_length=2000)


class Resposta(BaseModel):
    intencao: str
    resposta: str
    provider: str


@app.post("/atender", response_model=Resposta)
def atender(msg: Mensagem) -> Resposta:
    intent_raw = _llm.complete(msg.mensagem, system=PROMPT_INTENT).text.strip().lower()
    intent = next((i for i in INTENCOES if i in intent_raw), "outro")
    resp = _llm.complete(msg.mensagem, system=PROMPT_RESP).text.strip()
    return Resposta(intencao=intent, resposta=resp, provider=_llm.provider)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "provider": _llm.provider}
