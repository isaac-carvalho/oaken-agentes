"""Guardrails minimalistas: PII redaction, toxicity check e audit log."""
from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)

PII_PATTERNS = {
    "cpf": re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "phone": re.compile(r"\b(?:\+?55\s?)?\(?\d{2}\)?\s?\d{4,5}-?\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d{4}[- ]?){3}\d{1,4}\b"),
    "passport": re.compile(r"\b[A-Z]{1,2}\d{6,9}\b"),
    "cnpj": re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b"),
    "rg": re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dXx]\b"),
}

DEFAULT_BLOCKED_TERMS: set[str] = {"matar", "suicídio", "violência explícita"}
BLOCKED_TERMS = DEFAULT_BLOCKED_TERMS


@dataclass
class GuardrailResult:
    text: str
    redactions: dict[str, int]
    blocked: bool
    reason: str | None


def redact(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for tag, pat in PII_PATTERNS.items():
        out, n = pat.subn(f"[REDACTED:{tag}]", text)
        if n:
            counts[tag] = n
            text = out
    return text, counts


def check_toxicity(text: str, blocked_terms: set[str] | None = None) -> tuple[bool, str | None]:
    """Verifica toxicidade. Se blocked_terms for passado, usa-o em vez do default."""
    terms = blocked_terms if blocked_terms is not None else BLOCKED_TERMS
    lower = text.lower()
    for term in terms:
        if term in lower:
            return True, f"contém termo bloqueado: {term}"
    return False, None


def audit(path: Path, payload: dict) -> None:
    payload = {**payload, "ts": datetime.now(timezone.utc).isoformat()}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def safe_call(client, prompt: str, audit_path: Path = Path("audit.log")) -> GuardrailResult:
    safe_prompt, redactions = redact(prompt)
    prompt_hash = hashlib.sha256(safe_prompt.encode("utf-8")).hexdigest()[:16]
    blocked, reason = check_toxicity(prompt)
    if blocked:
        audit(audit_path, {"event": "blocked_input", "hash": prompt_hash, "reason": reason})
        return GuardrailResult(text="", redactions=redactions, blocked=True, reason=reason)
    resp = client.complete(safe_prompt)
    out_blocked, out_reason = check_toxicity(resp.text)
    audit(
        audit_path,
        {
            "event": "completion",
            "hash": prompt_hash,
            "provider": getattr(client, "provider", "?"),
            "redactions": redactions,
            "out_blocked": out_blocked,
        },
    )
    if out_blocked:
        return GuardrailResult(text="", redactions=redactions, blocked=True, reason=out_reason)
    return GuardrailResult(text=resp.text, redactions=redactions, blocked=False, reason=None)
