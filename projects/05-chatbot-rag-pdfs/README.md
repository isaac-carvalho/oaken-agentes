# 05 — Chatbot RAG sobre PDFs

> **Carreira Alura:** Especialista em IA — Nível 1 (*RAG*)

App Streamlit que indexa PDFs locais (chunking + embeddings) num **ChromaDB**, e responde perguntas citando trechos.

## Stack
| Camada | Tecnologia |
|--------|------------|
| UI | `streamlit` |
| Orquestração | `langchain` |
| Vector store | `chromadb` |
| Embeddings | `sentence-transformers` (offline) ou OpenAI |
| LLM | `_shared` |

## Como rodar

```bash
pip install -r requirements.txt
mkdir -p docs
# coloque seus PDFs em ./docs
streamlit run app.py
```

Interface: upload de PDFs, botão "Reindexar", caixa de pergunta, resposta com trechos citados.

## Output de exemplo

Pipeline RAG validado headless (sem subir Streamlit):

```bash
$ python -c "from app import ingest_pdfs, answer; \
    print('chunks:', ingest_pdfs()); \
    r, f = answer('Qual modelo de embeddings o projeto usa?'); \
    print(r); print(f[:2])"
chunks: 2
[mock-llm:...] Resposta simulada para prompt de 1020 chars. ...
[{'file': 'oaken-rag.pdf', 'page': 1, 'trecho': 'Oaken Agentes — Portfolio...'},
 {'file': 'oaken-rag.pdf', 'page': 1, 'trecho': 'ndo a indexacao e a recuperacao corretas.'}]
```

A query traz os chunks corretos com metadata (`file`, `page`). Com `OPENAI_API_KEY`, o LLM substitui o placeholder mock por uma resposta narrativa citando fontes no formato `[arquivo p.X]`.

### Embeddings: padrão e fallback offline

Por padrão usa `sentence-transformers/all-MiniLM-L6-v2` (alta qualidade semântica). Se não houver acesso ao HuggingFace Hub (ex: ambientes air-gapped), cai automaticamente para um `_HashEmbedder` interno (feature hashing, 384 dims) — pior em qualidade mas garante o pipeline operacional.

## Entregáveis para portfólio
- RAG completo end-to-end
- Funciona offline com embeddings locais (`sentence-transformers`)
- Citação de fontes (página + trecho)
