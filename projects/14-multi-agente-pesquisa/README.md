# 14 — Sistema Multi-Agente de Pesquisa

> **Carreira Alura:** Engenharia de Agentes — Nível 1

Três agentes colaborando para produzir um relatório técnico:
1. **Pesquisador** — coleta tópicos e fontes (DuckDuckGo)
2. **Crítico** — valida cobertura e aponta lacunas
3. **Escritor** — produz o relatório final em Markdown

Implementado com **LangGraph** (não depende de framework opinado tipo CrewAI; mais didático).

## Stack
| Camada | Tecnologia |
|--------|------------|
| Orquestração | `langgraph` |
| Web search | `duckduckgo-search` |
| LLM | `_shared` |

## Como rodar

```bash
pip install -r requirements.txt
python main.py "tendências de agentes de IA em 2026"
cat out/relatorio.md
```

## Entregáveis para portfólio
- Padrão multi-agente com handoff explícito
- Loop de revisão (crítico → escritor) limitado a N iterações
- Relatório final em Markdown
