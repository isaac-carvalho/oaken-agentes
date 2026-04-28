"""Testes do handler Lambda/Bedrock."""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from handler import MODEL_ID, SYSTEM, _bedrock_call, lambda_handler


def test_lambda_handler_missing_message():
    event = {"body": json.dumps({})}
    resp = lambda_handler(event, None)
    assert resp["statusCode"] == 400
    body = json.loads(resp["body"])
    assert "error" in body


def test_lambda_handler_empty_body():
    event = {"body": None}
    resp = lambda_handler(event, None)
    assert resp["statusCode"] == 400


def test_lambda_handler_success_mock_fallback():
    event = {"body": json.dumps({"message": "Olá"})}
    # Without boto3 configured, falls into except → mock response
    resp = lambda_handler(event, None)
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert "reply" in body
    assert "model" in body


def test_lambda_handler_with_mocked_bedrock():
    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps({
        "content": [{"text": "Resposta do Claude", "type": "text"}]
    }).encode()
    mock_client = MagicMock()
    mock_client.invoke_model.return_value = {"body": mock_body}

    import boto3 as _  # noqa: F401 — ensure module exists for patching
    with patch("boto3.client", return_value=mock_client):
        result = _bedrock_call("Olá Bedrock")
        assert result == "Resposta do Claude"


def test_lambda_handler_bedrock_error_fallback():
    event = {"body": json.dumps({"message": "test"})}
    with patch("handler._bedrock_call", side_effect=RuntimeError("no creds")):
        resp = lambda_handler(event, None)
        assert resp["statusCode"] == 200
        body = json.loads(resp["body"])
        assert "mock-bedrock" in body["reply"]


def test_lambda_handler_returns_json_content_type():
    event = {"body": json.dumps({"message": "test"})}
    resp = lambda_handler(event, None)
    assert resp["headers"]["content-type"] == "application/json"


def test_model_id_default():
    assert "claude" in MODEL_ID or "anthropic" in MODEL_ID
