"""Testes do toolkit LGPD."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Patch LOG and CONSENT_DB before importing api
_tmp_dir = tempfile.mkdtemp()
_test_log = Path(_tmp_dir) / "test_audit.log"
_test_consent = Path(_tmp_dir) / "test_consent.json"

import api

api.LOG = _test_log
api.CONSENT_DB = _test_consent

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def clean_files():
    """Limpa ficheiros de teste antes de cada test."""
    if _test_log.exists():
        _test_log.unlink()
    if _test_consent.exists():
        _test_consent.unlink()
    yield


# --- Anonimização ---

def test_anonimizar_cpf():
    resp = client.post("/anonimizar", json={"texto": "CPF 123.456.789-00"})
    assert resp.status_code == 200
    data = resp.json()
    assert "[CPF]" in data["texto"]
    assert data["encontrados"]["cpf"] == 1


def test_anonimizar_email():
    resp = client.post("/anonimizar", json={"texto": "Email: user@test.com"})
    data = resp.json()
    assert "[EMAIL]" in data["texto"]


def test_anonimizar_phone():
    resp = client.post("/anonimizar", json={"texto": "Fone: 11 98765-4321"})
    data = resp.json()
    assert "[PHONE]" in data["texto"]


def test_anonimizar_rg():
    resp = client.post("/anonimizar", json={"texto": "RG: 12.345.678-9"})
    data = resp.json()
    assert "[RG]" in data["texto"]


def test_anonimizar_no_pii():
    resp = client.post("/anonimizar", json={"texto": "Texto sem dados"})
    data = resp.json()
    assert data["encontrados"] == {}


# --- Consentimento ---

def test_registrar_consentimento():
    resp = client.post("/consentimento", json={
        "titular": "joao", "finalidade": "marketing", "aceito": True
    })
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


def test_consentimento_multiple_purposes():
    client.post("/consentimento", json={"titular": "ana", "finalidade": "marketing", "aceito": True})
    client.post("/consentimento", json={"titular": "ana", "finalidade": "analytics", "aceito": False})
    db = json.loads(_test_consent.read_text())
    assert "marketing" in db["ana"]
    assert "analytics" in db["ana"]
    assert db["ana"]["analytics"]["aceito"] is False


def test_consent_revocation():
    """Revogar consentimento anterior."""
    client.post("/consentimento", json={"titular": "bob", "finalidade": "ads", "aceito": True})
    client.post("/consentimento", json={"titular": "bob", "finalidade": "ads", "aceito": False})
    db = json.loads(_test_consent.read_text())
    assert db["bob"]["ads"]["aceito"] is False


# --- Exclusão / Direito ao esquecimento ---

def test_excluir_titular():
    client.post("/consentimento", json={"titular": "maria", "finalidade": "x", "aceito": True})
    resp = client.delete("/titular/maria")
    assert resp.json()["removido"] is True
    # Verify data is gone
    db = json.loads(_test_consent.read_text())
    assert "maria" not in db


def test_excluir_titular_inexistente():
    resp = client.delete("/titular/fantasma")
    assert resp.json()["removido"] is False


def test_deletion_cascade():
    """Exclusão deve remover todas as finalidades do titular."""
    client.post("/consentimento", json={"titular": "ze", "finalidade": "a", "aceito": True})
    client.post("/consentimento", json={"titular": "ze", "finalidade": "b", "aceito": True})
    client.post("/consentimento", json={"titular": "ze", "finalidade": "c", "aceito": True})
    resp = client.delete("/titular/ze")
    assert resp.json()["removido"] is True
    db = json.loads(_test_consent.read_text())
    assert "ze" not in db


# --- Auditoria ---

def test_auditoria_empty():
    resp = client.get("/auditoria")
    assert resp.status_code == 200
    assert resp.json() == []


def test_auditoria_after_operations():
    client.post("/anonimizar", json={"texto": "CPF 111.222.333-44"})
    resp = client.get("/auditoria")
    records = resp.json()
    assert len(records) >= 1
    assert records[0]["event"] == "anonimize"


def test_verificar_chain_empty():
    resp = client.get("/auditoria/verificar")
    assert resp.json()["valido"] is True
    assert resp.json()["n"] == 0


def test_verificar_chain_after_operations():
    client.post("/anonimizar", json={"texto": "Email a@b.com"})
    client.post("/consentimento", json={"titular": "x", "finalidade": "y", "aceito": True})
    resp = client.get("/auditoria/verificar")
    assert resp.json()["valido"] is True
    assert resp.json()["n"] == 2


# --- Consent status endpoint ---

def test_consent_status():
    client.post("/consentimento", json={"titular": "ana", "finalidade": "ads", "aceito": True})
    client.post("/consentimento", json={"titular": "ana", "finalidade": "email", "aceito": False})
    resp = client.get("/consentimento/ana")
    assert resp.status_code == 200
    data = resp.json()
    assert data["titular"] == "ana"
    assert "ads" in data["finalidades"]


def test_consent_status_not_found():
    resp = client.get("/consentimento/naoexiste")
    assert resp.status_code == 404
