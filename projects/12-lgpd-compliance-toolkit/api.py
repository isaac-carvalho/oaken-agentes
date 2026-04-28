"""Toolkit de compliance LGPD."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

PII = {
    "cpf": re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "phone": re.compile(r"\b(?:\+?55\s?)?\(?\d{2}\)?\s?\d{4,5}-?\d{4}\b"),
    "rg": re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dXx]\b"),
}

LOG = Path(__file__).parent / "audit_chain.log"
CONSENT_DB = Path(__file__).parent / "consent.json"

app = FastAPI(title="LGPD Toolkit")


class TextoIn(BaseModel):
    texto: str


class Consentimento(BaseModel):
    titular: str
    finalidade: str
    aceito: bool


def _last_hash() -> str:
    if not LOG.exists():
        return "0" * 64
    last = LOG.read_text(encoding="utf-8").splitlines()[-1] if LOG.stat().st_size else ""
    if not last:
        return "0" * 64
    return json.loads(last)["hash"]


def _append(event: dict) -> str:
    prev = _last_hash()
    payload = {**event, "prev": prev, "ts": datetime.now(timezone.utc).isoformat()}
    h = hashlib.sha256((prev + json.dumps(payload, sort_keys=True)).encode()).hexdigest()
    payload["hash"] = h
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return h


def anonimize(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for tag, pat in PII.items():
        text, n = pat.subn(f"[{tag.upper()}]", text)
        if n:
            counts[tag] = n
    return text, counts


def _load_consent() -> dict:
    if CONSENT_DB.exists():
        return json.loads(CONSENT_DB.read_text(encoding="utf-8"))
    return {}


def _save_consent(d: dict) -> None:
    CONSENT_DB.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


@app.post("/anonimizar")
def anonimizar(payload: TextoIn) -> dict:
    safe, found = anonimize(payload.texto)
    h = _append({"event": "anonimize", "found": found})
    return {"texto": safe, "encontrados": found, "audit_hash": h}


@app.post("/consentimento")
def registrar_consentimento(c: Consentimento) -> dict:
    db = _load_consent()
    db.setdefault(c.titular, {})[c.finalidade] = {
        "aceito": c.aceito,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    _save_consent(db)
    h = _append({"event": "consent", "titular": c.titular, "finalidade": c.finalidade, "aceito": c.aceito})
    return {"ok": True, "audit_hash": h}


@app.get("/consentimento/{titular_id}")
def consultar_consentimento(titular_id: str) -> dict:
    """Consulta status de consentimento de um titular."""
    db = _load_consent()
    if titular_id not in db:
        raise HTTPException(404, f"Titular '{titular_id}' não encontrado")
    return {"titular": titular_id, "finalidades": db[titular_id]}


@app.delete("/titular/{titular_id}")
def excluir(titular_id: str) -> dict:
    """Direito ao esquecimento (LGPD art. 18) com cascade completo."""
    db = _load_consent()
    existed = titular_id in db
    purposes_removed = list(db.get(titular_id, {}).keys())
    db.pop(titular_id, None)
    _save_consent(db)
    h = _append({
        "event": "erase",
        "titular": titular_id,
        "existia": existed,
        "finalidades_removidas": purposes_removed,
    })
    return {"removido": existed, "finalidades_removidas": purposes_removed, "audit_hash": h}


@app.get("/auditoria")
def auditoria(limit: int = 50) -> list[dict]:
    if not LOG.exists():
        return []
    lines = LOG.read_text(encoding="utf-8").splitlines()[-limit:]
    return [json.loads(line) for line in lines]


@app.get("/auditoria/verificar")
def verificar_chain() -> dict:
    if not LOG.exists():
        return {"valido": True, "n": 0}
    prev = "0" * 64
    n = 0
    for line in LOG.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        n += 1
        if rec["prev"] != prev:
            raise HTTPException(500, f"chain quebrado no registro {n}")
        recomputed = hashlib.sha256(
            (prev + json.dumps({k: v for k, v in rec.items() if k != "hash"}, sort_keys=True)).encode()
        ).hexdigest()
        if recomputed != rec["hash"]:
            raise HTTPException(500, f"hash inválido no registro {n}")
        prev = rec["hash"]
    return {"valido": True, "n": n}
