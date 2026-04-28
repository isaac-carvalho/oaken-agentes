"""Benchmark side-by-side de LLMs."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared.env import get_env  # noqa: E402
from projects._shared.llm_clients import (  # noqa: E402
    AnthropicClient,
    GeminiClient,
    LLMResponse,
    MockLLMClient,
    OpenAIClient,
)

TASKS = {
    "Resumir": "Resuma em 2 frases: A inteligência artificial está transformando indústrias inteiras, automatizando tarefas e gerando novos modelos de negócio.",
    "Classificar sentimento": "Classifique como POSITIVO/NEUTRO/NEGATIVO: 'Demorou bastante mas no fim valeu a pena.'",
    "Gerar código": "Função Python que recebe lista de dicts e devolve média de uma chave específica.",
}


def call_ollama(model: str, prompt: str) -> LLMResponse:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=60,
    )
    r.raise_for_status()
    return LLMResponse(text=r.json().get("response", ""), model=model, provider="ollama")


def build_clients() -> dict[str, object]:
    clients: dict[str, object] = {}
    if k := get_env("OPENAI_API_KEY"):
        clients["openai/gpt-4o-mini"] = OpenAIClient(k, "gpt-4o-mini")
    if k := (get_env("GEMINI_API_KEY") or get_env("GOOGLE_API_KEY")):
        clients["gemini/flash"] = GeminiClient(k, "gemini-1.5-flash")
    if k := get_env("ANTHROPIC_API_KEY"):
        clients["anthropic/haiku"] = AnthropicClient(k, "claude-haiku-4-5")
    clients["ollama/llama3.2"] = "ollama:llama3.2"  # marker
    if not any(k for k in (get_env("OPENAI_API_KEY"), get_env("GEMINI_API_KEY"), get_env("ANTHROPIC_API_KEY"))):
        clients["mock"] = MockLLMClient()
    return clients


st.set_page_config(page_title="Benchmark LLMs", layout="wide")
st.title("⚡ Benchmark LLMs")

clients = build_clients()
selected = st.multiselect("Modelos", list(clients), default=list(clients))
task_name = st.selectbox("Tarefa", list(TASKS))
prompt = st.text_area("Prompt", TASKS[task_name], height=150)

if st.button("Rodar"):
    rows = []
    for name in selected:
        c = clients[name]
        t0 = time.perf_counter()
        try:
            if isinstance(c, str) and c.startswith("ollama:"):
                resp = call_ollama(c.split(":", 1)[1], prompt)
            else:
                resp = c.complete(prompt)
            text, err = resp.text, ""
        except Exception as e:
            text, err = "", str(e)
        ms = int((time.perf_counter() - t0) * 1000)
        rows.append({"modelo": name, "latência_ms": ms, "erro": err, "resposta": text[:400]})
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
