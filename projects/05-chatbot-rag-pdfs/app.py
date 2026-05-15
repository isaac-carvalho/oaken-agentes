"""Streamlit UI para chatbot RAG sobre PDFs locais."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from projects._shared import get_default_client  # noqa: E402

DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma"
COLLECTION = "pdfs"


class _HashEmbedder:
    """Fallback offline: embedding por feature hashing (bag-of-words). Não substitui
    um embedder semântico real, mas garante o pipeline RAG funcional sem internet."""

    def __init__(self, dim: int = 384) -> None:
        self.dim = dim

    def name(self) -> str:
        return "hash-embedder-384"

    def _embed_one(self, text: str) -> list[float]:
        import hashlib

        v = [0.0] * self.dim
        for word in text.lower().split():
            idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % self.dim
            v[idx] += 1.0
        norm = sum(x * x for x in v) ** 0.5
        return [x / norm for x in v] if norm > 0 else v

    def __call__(self, input):
        return [self._embed_one(t) for t in input]

    def embed_documents(self, input):
        return self.__call__(input)

    def embed_query(self, input):
        if isinstance(input, str):
            return self._embed_one(input)
        return [self._embed_one(t) for t in input]


@st.cache_resource
def get_collection():
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    embedder = None
    try:
        from chromadb.utils import embedding_functions

        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        # Força carregar o modelo agora, para falhar cedo se não houver internet.
        embedder(["warmup"])
    except Exception:
        embedder = _HashEmbedder()
    return client.get_or_create_collection(COLLECTION, embedding_function=embedder)


def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    """Divide texto em chunks respeitando limites de palavras (quebra em \\n)."""
    chunks: list[str] = []
    lines = text.split("\n")
    current: list[str] = []
    current_len = 0
    for line in lines:
        line_len = len(line) + 1  # +1 para o \n
        if current_len + line_len > size and current:
            chunk = "\n".join(current)
            chunks.append(chunk)
            # overlap: mantém últimas linhas até atingir overlap chars
            overlap_lines: list[str] = []
            overlap_len = 0
            for prev_line in reversed(current):
                if overlap_len + len(prev_line) + 1 > overlap:
                    break
                overlap_lines.insert(0, prev_line)
                overlap_len += len(prev_line) + 1
            current = overlap_lines
            current_len = overlap_len
        current.append(line)
        current_len += line_len
    if current:
        chunks.append("\n".join(current))
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
