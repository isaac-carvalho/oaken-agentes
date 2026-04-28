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

## Output de exemplo

### Tools isoladas (validadas)
```bash
$ python -c "from main import tool_calc, tool_python, tool_web; \
    print('CALC:', tool_calc('2*3.14159*5')); \
    print('PY:', tool_python('print(sum(range(10)))')); \
    print('WEB:', tool_web('python language')[:120])"
CALC: 31.4159
PY: 45
WEB: - Python (programming language) - Wikipedia: Python is a high-level, general-purpose ...
```

### Loop ReAct
Sem `OPENAI_API_KEY` o `MockLLMClient` devolve placeholder e o loop encerra com `(sem ação parseável)` — esperado, pois ReAct exige um LLM real para decidir qual tool chamar.

Com chave real:
```bash
$ python main.py "qual a raiz quadrada de 12345 vezes pi?"
--- step 0 ---
PENSAMENTO: Preciso calcular sqrt(12345) * pi
ACAO: {"tool": "calc", "input": "sqrt(12345)*3.14159265"}
OBSERVACAO: 348.96...

--- step 1 ---
FINAL: A raiz quadrada de 12345 multiplicada por pi é aproximadamente 348.96.
```

## Entregáveis para portfólio
- Loop ReAct ilustrativo (não black-box do LangChain)
- 3 tools com descrição clara
- Logs do raciocínio passo-a-passo
