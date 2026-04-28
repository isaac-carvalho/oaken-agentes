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

## Output de exemplo

```bash
$ python main.py "tendências de agentes de IA em 2026"
Relatório salvo em out/relatorio.md
```

Pipeline executado: **pesquisador** chama DuckDuckGo (4 sub-tópicos), **crítico** avalia cobertura, **escritor** produz o relatório final em markdown — tudo orquestrado por um grafo LangGraph com aresta condicional (re-pesquisa se o crítico não disser OK, até max 1 iteração extra).

> Sem `OPENAI_API_KEY` o relatório fica curto (output do `MockLLMClient`). Com chave real o markdown sai com 600-1500 palavras citando os snippets do DDG.

> ⚠️ Nota técnica: a lib `duckduckgo-search` foi renomeada para `ddgs`. O código tenta `from ddgs import DDGS` primeiro e cai no nome antigo se necessário.

## Entregáveis para portfólio
- Padrão multi-agente com handoff explícito
- Loop de revisão (crítico → escritor) limitado a N iterações
- Relatório final em Markdown
