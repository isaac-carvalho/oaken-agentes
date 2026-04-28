# 07 — Agente com Tools (Zero-Shot)

> **Carreira Alura:** Especialista em IA — Nível 2 (*Agentes e modelos*)

Agente conversacional que decide, a cada turno, qual ferramenta usar entre: calculadora, busca web (DuckDuckGo) e execução de Python em sandbox. Implementa o padrão **ReAct** (raciocínio + ação) sem framework pesado.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Loop ReAct | implementação própria |
| Tools | `duckduckgo-search`, `numexpr`, `subprocess` (sandbox) |
| LLM | `_shared` |

## Como rodar

```bash
pip install -r requirements.txt
python main.py "qual a raiz quadrada de 12345 vezes pi?"
python main.py "quem ganhou a copa do mundo de 2022 e em que país foi?"
```

## Entregáveis para portfólio
- Loop ReAct ilustrativo (não black-box do LangChain)
- 3 tools com descrição clara
- Logs do raciocínio passo-a-passo
