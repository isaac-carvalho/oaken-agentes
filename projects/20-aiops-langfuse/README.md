# 20 — AIOps: Observabilidade de Agentes com Langfuse

> **Carreira Alura:** Engenharia de Agentes — Nível 3 (*AIOps*)

Instrumenta um agente LLM com **Langfuse** para coletar traces (cada chamada vira um span), avaliações automáticas e alertas. Funciona com Langfuse cloud ou self-hosted. Sem credenciais, cai num **modo sink local** que escreve traces em `traces.jsonl`.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Observabilidade | `langfuse` (com fallback local) |
| Agente | `_shared` LLM clients |

## Como rodar

```bash
pip install -r requirements.txt
# Para usar Langfuse real, defina LANGFUSE_PUBLIC_KEY e LANGFUSE_SECRET_KEY no .env
python main.py "qual a capital da França?"
python main.py "explique microsserviços"
cat traces.jsonl   # se rodando em modo local
```

## Output de exemplo

Sem credenciais Langfuse, cai no `LocalSink` que escreve traces estruturados em `traces.jsonl`:

```bash
$ python main.py "qual a capital da França?"
[obs] modo=local
score=0.721
[mock-llm:...] Resposta simulada ...

$ python main.py "explique microsserviços em uma frase"
[obs] modo=local
score=0.721
...

$ cat traces.jsonl
{"name":"agent_chat","input":{"question":"qual a capital..."},
 "output":{"text":"[mock-llm:..."},
 "metadata":{"provider":"mock","score":0.721},
 "latency_ms":0,"ts":"2026-04-28T09:50:44.559680+00:00"}
{"name":"agent_chat","input":{"question":"explique microsserviços..."},...}
```

Cada trace tem `input`, `output`, `latency_ms`, `metadata` (provider + score de qualidade). Com `LANGFUSE_PUBLIC_KEY` + `LANGFUSE_SECRET_KEY` no `.env`, a saída muda para `[obs] modo=langfuse` e os spans aparecem na UI cloud/self-hosted.

## Entregáveis para portfólio
- Tracing estruturado de uma cadeia LLM
- Avaliação automática (heurística de qualidade no output)
- Demonstra cultura de observabilidade em produção
