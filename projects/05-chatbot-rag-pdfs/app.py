"""Streamlit UI para chatbot RAG sobre PDFs locais."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma"
COLLECTION = "pdfs"


@st.cache_resource
def get_collection():
    import chromadb
    from chromadb.utils import embedding_functions

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(COLLECTION, embedding_function=embedder)


def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    chunks: list[str] = []
    i = 0
    while i < len(text):
        chunks.append(text[i : i + size])
        i += size - overlap
    return chunks


def ingest_pdfs() -> int:
    from pypdf import PdfReader

    coll = get_collection()
    DOCS_DIR.mkdir(exist_ok=True)
    added = 0
    for pdf in DOCS_DIR.glob("*.pdf"):
        reader = PdfReader(str(pdf))
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            for ck_idx, chunk in enumerate(chunk_text(text)):
                if not chunk.strip():
                    continue
                doc_id = f"{pdf.name}::p{page_idx}::c{ck_idx}"
                coll.upsert(
                    documents=[chunk],
                    ids=[doc_id],
                    metadatas=[{"file": pdf.name, "page": page_idx + 1}],
                )
                added += 1
    return added


def answer(question: str, k: int = 4) -> tuple[str, list[dict]]:
    coll = get_collection()
    res = coll.query(query_texts=[question], n_results=k)
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    context = "\n\n---\n\n".join(
        f"[{m['file']} p.{m['page']}] {d}" for d, m in zip(docs, metas)
    )
    client = get_default_client()
    prompt = (
        "Responda em português, citando as fontes no formato [arquivo p.X]. "
        "Se a resposta não estiver no contexto, diga claramente.\n\n"
        f"Contexto:\n{context}\n\nPergunta: {question}"
    )
    resp = client.complete(prompt, system="Você é um assistente RAG preciso.")
    return resp.text, [{"file": m["file"], "page": m["page"], "trecho": d[:200]} for d, m in zip(docs, metas)]


st.set_page_config(page_title="Chatbot RAG PDFs", layout="wide")
st.title("📚 Chatbot RAG sobre PDFs")

with st.sidebar:
    st.subheader("Indexação")
    if st.button("(Re)indexar PDFs em ./docs"):
        n = ingest_pdfs()
        st.success(f"{n} chunks adicionados.")
    st.caption(f"Diretório: {DOCS_DIR}")

q = st.text_input("Pergunta:", placeholder="Sobre o que fala o documento?")
if q:
    with st.spinner("Buscando..."):
        resp, fontes = answer(q)
    st.markdown(resp)
    with st.expander("Fontes"):
        for f in fontes:
            st.write(f)
