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

## Output de exemplo

### Sandbox isolado (validado)

```bash
$ python -c "from sandbox import run_in_docker; \
    ok, out = run_in_docker('print(sum(range(100)))'); \
    print('OK:', ok, '| OUT:', out.strip())"
OK: True | OUT: 4950

$ python -c "from sandbox import run_in_docker; \
    ok, out = run_in_docker('def is_prime(n): return n>1 and all(n%i for i in range(2,int(n**0.5)+1))\\nfor n,e in [(2,True),(7,True),(8,False)]: assert is_prime(n)==e\\nprint(\"OK\")'); \
    print('OK:', ok, '| OUT:', out.strip())"
OK: True | OUT: OK

$ python -c "from sandbox import run_in_docker; \
    ok, out = run_in_docker('raise ValueError(\"oops\")'); \
    print('OK:', ok, '| OUT:', out[:200].strip())"
OK: False | OUT: Traceback ... ValueError: oops
```

Sem Docker rodando, `run_in_docker` usa fallback `subprocess` com timeout 10s — o que demonstrei acima.

### Loop write→run→fix

Sem `OPENAI_API_KEY`, o `MockLLMClient` devolve placeholder; o agente tenta executar e falha com `SyntaxError` na primeira iteração — comportamento esperado, pois o loop precisa de um LLM real para escrever Python válido. Com chave real, o agente itera até passar (`OK` no stdout) ou esgotar `--max-iter` (default 5).

## Entregáveis para portfólio
- Loop write → run → fix com no máximo 5 iterações
- Sandbox real (Docker) demonstra preocupação com segurança
- Logs de cada iteração em `out/`
