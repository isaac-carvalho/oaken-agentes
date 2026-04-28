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

## Output de exemplo

Pipeline completo (ingest → agente com 4 nós) testado headless:

```bash
$ python ingest.py samples
1 chunks indexados.

$ python -c "from agent import build_graph; \
    g = build_graph(); \
    out = g.invoke({'question':'Sobre o que é o portfolio?', 'messages':[]}, \
                   {'configurable':{'thread_id':'demo'}}); \
    print(out['context'][:200]); print('FINAL:', out['final'][:200])"
# Sobre o portfólio Oaken Agentes
# Este portfólio contém 21 projetos práticos ...
FINAL: [mock-llm:988be6c2] Resposta simulada ...
```

O state machine roda os 4 nós em ordem (`retrieve → answer → critic → refine`); o `MemorySaver` persiste o histórico por `thread_id` (basta chamar invoke de novo com o mesmo id pra continuar a conversa).

> Sem API key, todos os 4 nós devolvem texto do `MockLLMClient` (o critic não decide "OK" porque o mock não responde com essa palavra, então o refine sempre roda — comportamento esperado).

### Embeddings: padrão e fallback offline

Mesmo padrão do projeto 05: `sentence-transformers/all-MiniLM-L6-v2` por default; `_HashEmbedder` (feature hashing 384d) como fallback quando HuggingFace está indisponível. Ver `embedder.py`.

## Entregáveis para portfólio
- LangGraph com 4 nós: retrieve → answer → critic → refine
- Memória persistente (Memorysaver)
- Diagrama do grafo em `graph.png` (gerado automaticamente)
