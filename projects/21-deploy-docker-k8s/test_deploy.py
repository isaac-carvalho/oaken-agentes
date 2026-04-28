"""Tests for project 21 — deploy-docker-k8s."""
from __future__ import annotations

from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

import pytest

# We need to mock _shared before importing app
sys.path.insert(0, str(Path(__file__).parent))


@pytest.fixture
def client():
    """Create FastAPI test client with mocked LLM."""
    mock_llm = MagicMock()
    mock_llm.provider = "mock"
    mock_response = MagicMock()
    mock_response.text = "Resposta teste"
    mock_response.provider = "mock"
    mock_response.model = "mock-1"
    mock_llm.complete.return_value = mock_response

    with patch("app.get_default_client", return_value=mock_llm), \
         patch("app._llm", mock_llm):
        # Re-import to get patched version
        import importlib
        import app as app_mod
        app_mod._llm = mock_llm
        from fastapi.testclient import TestClient
        return TestClient(app_mod.app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"


def test_health_has_dependencies(client):
    r = client.get("/health")
    data = r.json()
    assert "status" in data
    assert "dependencies" in data
    for dep in ("fastapi", "pydantic", "uvicorn"):
        assert data["dependencies"][dep] == "ok"


def test_ready(client):
    r = client.get("/ready")
    assert r.status_code == 200
    data = r.json()
    assert "provider" in data
    assert data["status"] == "ready"


def test_chat(client):
    r = client.post("/chat", json={"prompt": "Ola"})
    assert r.status_code == 200
    data = r.json()
    assert "reply" in data
    assert "provider" in data
    assert "model" in data


def test_chat_empty_prompt(client):
    r = client.post("/chat", json={"prompt": ""})
    assert r.status_code == 200


def test_chat_missing_prompt(client):
    r = client.post("/chat", json={})
    assert r.status_code == 422  # validation error
