"""Lambda handler que chama Bedrock Claude. Funciona localmente em modo mock."""
from __future__ import annotations

import json
import logging
import os

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-haiku-4-5")
SYSTEM = "Você é um assistente brasileiro, objetivo, em português."
MAX_MSG_LEN = 4000

_log = logging.getLogger("oaken.handler")
_log.setLevel(logging.INFO)


def _bedrock_call(message: str) -> str:
    import boto3

    client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": message}],
    })
    resp = client.invoke_model(modelId=MODEL_ID, body=body)
    payload = json.loads(resp["body"].read())
    return "".join(b.get("text", "") for b in payload.get("content", []))


def lambda_handler(event, _context):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"error": "JSON inválido"})}

    message = body.get("message", "")
    if not message or not isinstance(message, str):
        return {"statusCode": 400, "body": json.dumps({"error": "campo 'message' obrigatório"})}
    if len(message) > MAX_MSG_LEN:
        return {"statusCode": 400, "body": json.dumps({"error": f"message excede {MAX_MSG_LEN} chars"})}

    try:
        text = _bedrock_call(message)
        return {
            "statusCode": 200,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"reply": text, "model": MODEL_ID}, ensure_ascii=False),
        }
    except Exception as exc:
        # Log detalhado server-side; resposta genérica ao cliente (sem vazar infra).
        _log.exception("bedrock call failed")
        return {
            "statusCode": 503,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "serviço indisponível, tente novamente"}),
        }
