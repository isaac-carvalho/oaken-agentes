# 13 — Agente RAG com LangGraph

> **Carreira Alura:** Engenharia de Agentes — Nível 1 (*Construção de Agentes Inteligentes com RAG*)

Agente conversacional construído em **LangGraph** (state machine explícita) com:
- Memória conversacional por sessão
- RAG sobre base ChromaDB
- **Auto-correção**: nó crítico avalia a resposta e re-formula se ficar incompleta

## Stack
| Camada | Tecnologia |
|--------|------------|
| State machine | `langgraph` |
| RAG | `chromadb` + `sentence-transformers` |
| LLM | `_shared` |

## Como rodar

```bash
pip install -r requirements.txt
python ingest.py samples/        # popula ChromaDB
python chat.py                    # CLI conversacional
```

## Entregáveis para portfólio
- LangGraph com 4 nós: retrieve → answer → critic → refine
- Memória persistente (Memorysaver)
- Diagrama do grafo em `graph.png` (gerado automaticamente)
