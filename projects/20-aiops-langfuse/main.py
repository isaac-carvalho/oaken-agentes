"""Agente instrumentado com Langfuse (com fallback sink local)."""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import typer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402
from projects._shared.env import get_env  # noqa: E402

app = typer.Typer()
SINK = Path(__file__).parent / "traces.jsonl"


class LocalSink:
    """Sink que escreve traces como JSONL — usado quando Langfuse não está configurado."""

    def trace(self, **kwargs):
        return _LocalSpan(self, **kwargs)

    def emit(self, payload: dict) -> None:
        payload["ts"] = datetime.now(timezone.utc).isoformat()
        with SINK.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def flush(self) -> None:
        pass


class _LocalSpan:
    def __init__(self, sink: LocalSink, **meta) -> None:
        self.sink = sink
        self.meta = meta
        self.t0 = time.perf_counter()

    def update(self, **kwargs) -> None:
        self.meta.update(kwargs)

    def end(self) -> None:
        self.meta["latency_ms"] = int((time.perf_counter() - self.t0) * 1000)
        self.sink.emit(self.meta)


def get_langfuse():
    pub = get_env("LANGFUSE_PUBLIC_KEY")
    sec = get_env("LANGFUSE_SECRET_KEY")
    if not (pub and sec):
        return LocalSink(), "local"
    try:
        from langfuse import Langfuse

        return Langfuse(public_key=pub, secret_key=sec, host=get_env("LANGFUSE_HOST", "https://cloud.langfuse.com")), "langfuse"
    except Exception:
        return LocalSink(), "local"


def quality_score(text: str) -> float:
    """Heurística simples de qualidade: penaliza muito curto / muito repetitivo."""
    if not text:
        return 0.0
    words = text.split()
    uniq = len(set(words)) / max(len(words), 1)
    length_ok = 1.0 if 20 <= len(words) <= 400 else 0.5
    return round(0.5 * uniq + 0.5 * length_ok, 3)


@app.command()
def main(pergunta: str) -> None:
    sink, mode = get_langfuse()
    typer.echo(f"[obs] modo={mode}")
    span = sink.trace(name="agent_chat", input={"question": pergunta})
    client = get_default_client()
    resp = client.complete(pergunta, system="Responda em português, objetivo.")
    score = quality_score(resp.text)
    span.update(output={"text": resp.text}, metadata={"provider": client.provider, "score": score})
    span.end()
    if hasattr(sink, "flush"):
        sink.flush()
    typer.echo(f"\nscore={score}\n{resp.text}")


if __name__ == "__main__":
    app()
