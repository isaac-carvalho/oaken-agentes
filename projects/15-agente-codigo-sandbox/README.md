# 15 — Agente que Escreve, Executa e Debuga Código

> **Carreira Alura:** Engenharia de Agentes — Nível 1

Agente que recebe uma tarefa de código, **escreve**, **executa em sandbox Docker isolado**, vê o output, e **debuga** se falhar — tudo em loop até passar ou esgotar tentativas.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Orquestração | LangGraph |
| Sandbox | Docker (`python:3.12-slim`) com network=none |
| LLM | `_shared` |

## Como rodar

Pré-requisito: Docker rodando.
```bash
pip install -r requirements.txt
python main.py "função is_prime que recebe int e devolve bool, com 5 testes assert"
```

Sem Docker: cai num modo "subprocess restrito" que executa em `subprocess` com timeout (menos seguro, ok para demo).

## Entregáveis para portfólio
- Loop write → run → fix com no máximo 5 iterações
- Sandbox real (Docker) demonstra preocupação com segurança
- Logs de cada iteração em `out/`
