"""Testes dos guardrails LLM."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.llm_clients import LLMResponse

from guardrails import (
    BLOCKED_TERMS,
    PII_PATTERNS,
    GuardrailResult,
    audit,
    check_toxicity,
    redact,
    safe_call,
)


# --- PII redaction ---

def test_redact_cpf():
    text, counts = redact("Meu CPF é 123.456.789-00 e pronto")
    assert "[REDACTED:cpf]" in text
    assert counts["cpf"] == 1


def test_redact_email():
    text, counts = redact("Contato: joao@empresa.com.br")
    assert "[REDACTED:email]" in text
    assert counts["email"] == 1


def test_redact_phone():
    text, counts = redact("Me liga em +55 11 98765-4321")
    assert "[REDACTED:phone]" in text
    assert counts["phone"] == 1


def test_redact_credit_card():
    text, counts = redact("Cartão: 4111 1111 1111 1111")
    assert "[REDACTED:credit_card]" in text
    assert counts["credit_card"] == 1


def test_redact_passport():
    text, counts = redact("Passaporte: AB123456")
    assert "[REDACTED:passport]" in text
    assert counts["passport"] == 1


def test_redact_no_pii():
    text, counts = redact("Apenas texto normal sem dados sensíveis")
    assert counts == {}
    assert "REDACTED" not in text


def test_redact_multiple_pii():
    text, counts = redact("CPF 123.456.789-00 email a@b.com fone 11 98765-4321")
    assert len(counts) >= 2


# --- Toxicity ---

def test_check_toxicity_blocked():
    blocked, reason = check_toxicity("Quero matar o processo")
    assert blocked is True
    assert reason is not None


def test_check_toxicity_clean():
    blocked, reason = check_toxicity("Bom dia, como vai?")
    assert blocked is False
    assert reason is None


def test_check_toxicity_case_insensitive():
    blocked, _ = check_toxicity("SUICÍDIO é tema sério")
    assert blocked is True


def test_check_toxicity_configurable():
    """Toxicity filter should accept custom blocked terms."""
    blocked, reason = check_toxicity("Texto com spam", blocked_terms={"spam"})
    assert blocked is True
    assert "spam" in reason


def test_check_toxicity_configurable_empty():
    blocked, _ = check_toxicity("matar algo", blocked_terms=set())
    assert blocked is False


# --- Audit ---

def test_audit_writes_jsonl():
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        p = Path(f.name)
    audit(p, {"event": "test", "data": 42})
    lines = p.read_text().strip().split("\n")
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["event"] == "test"
    assert "ts" in rec
    p.unlink()


# --- safe_call integration ---

def test_safe_call_normal():
    client = MagicMock()
    client.provider = "mock"
    client.complete.return_value = LLMResponse(text="Tudo bem", model="m", provider="mock")
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        p = Path(f.name)
    result = safe_call(client, "Olá", audit_path=p)
    assert result.blocked is False
    assert result.text == "Tudo bem"
    p.unlink()


def test_safe_call_blocks_toxic_input():
    client = MagicMock()
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        p = Path(f.name)
    result = safe_call(client, "Quero matar todos", audit_path=p)
    assert result.blocked is True
    client.complete.assert_not_called()
    p.unlink()


def test_safe_call_blocks_toxic_output():
    client = MagicMock()
    client.provider = "mock"
    client.complete.return_value = LLMResponse(text="Vá se matar", model="m", provider="mock")
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        p = Path(f.name)
    result = safe_call(client, "Diga algo", audit_path=p)
    assert result.blocked is True
    assert result.text == ""
    p.unlink()


def test_safe_call_redacts_pii_before_sending():
    client = MagicMock()
    client.provider = "mock"
    client.complete.return_value = LLMResponse(text="ok", model="m", provider="mock")
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        p = Path(f.name)
    safe_call(client, "Email joao@x.com e CPF 111.222.333-44", audit_path=p)
    sent_prompt = client.complete.call_args[0][0]
    assert "joao@x.com" not in sent_prompt
    assert "111.222.333-44" not in sent_prompt
    p.unlink()
