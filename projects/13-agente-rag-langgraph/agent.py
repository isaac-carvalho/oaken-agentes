"""Grafo LangGraph: retrieve → answer → critic → refine."""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Annotated, TypedDict

log = logging.getLogger(__name__)

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

CHROMA_DIR = Path(__file__).parent / "chroma"
COLLECTION = "knowledge"


class State(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    context: str
    draft: str
    critique: str
    final: str


def _retrieve_node(state: State) -> dict:
    import chromadb

    from embedder import get_embedder

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    coll = client.get_or_create_collection(COLLECTION, embedding_function=get_embedder())
    res = coll.query(query_texts=[state["question"]], n_results=4)
    ctx = "\n---\n".join(res["documents"][0]) if res["documents"] else ""
    return {"context": ctx}


def _answer_node(state: State) -> dict:
    llm = get_default_client()
    prompt = f"Pergunta: {state['question']}\n\nContexto:\n{state['context']}\n\nResposta:"
    return {"draft": llm.complete(prompt, system="Responda em português, baseado no contexto.").text}


def _critic_node(state: State) -> dict:
    llm = get_default_client()
    prompt = (
        f"Pergunta: {state['question']}\n\nResposta proposta:\n{state['draft']}\n\n"
        "Avalie em 1 frase se está completa e factual. Comece com OK ou MELHORAR."
    )
    return {"critique": llm.complete(prompt, system="Você é um revisor crítico.").text}


def _refine_node(state: State) -> dict:
    if state["critique"].strip().upper().startswith("OK"):
        return {"final": state["draft"]}
    llm = get_default_client()
    prompt = (
        f"Pergunta: {state['question']}\nContexto:\n{state['context']}\n"
        f"Rascunho:\n{state['draft']}\nCrítica:\n{state['critique']}\n\nProduza versão final melhorada."
    )
    return {"final": llm.complete(prompt, system="Responda em português, factual e completo.").text}


def build_graph():
    g = StateGraph(State)
    g.add_node("retrieve", _retrieve_node)
    g.add_node("answer", _answer_node)
    g.add_node("critic", _critic_node)
    g.add_node("refine", _refine_node)
    g.add_edge(START, "retrieve")
    g.add_edge("retrieve", "answer")
    g.add_edge("answer", "critic")
    g.add_edge("critic", "refine")
    g.add_edge("refine", END)
    return g.compile(checkpointer=MemorySaver())
