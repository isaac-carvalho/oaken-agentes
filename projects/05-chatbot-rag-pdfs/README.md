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

## Entregáveis para portfólio
- RAG completo end-to-end
- Funciona offline com embeddings locais (`sentence-transformers`)
- Citação de fontes (página + trecho)
