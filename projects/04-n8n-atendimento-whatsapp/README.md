# 04 — n8n + Atendimento WhatsApp

> **Carreira Alura:** Especialista em IA — Nível 1 (*N8N, Chatbots e RAG*)

Workflow no **n8n** que recebe uma mensagem de WhatsApp via webhook, classifica a intenção (saudação, dúvida, reclamação) e responde via LLM. O fluxo n8n chama uma API FastAPI deste projeto que faz a classificação + geração da resposta.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Orquestração | n8n (workflow JSON) |
| API | FastAPI |
| LLM | `_shared` |

## Como rodar

```bash
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
# Em outro terminal:
curl -X POST http://localhost:8000/atender \
  -H 'content-type: application/json' \
  -d '{"telefone":"+5511...","mensagem":"meu pedido não chegou"}'
```

Importe `workflow.json` no n8n (Settings → Import from file) e aponte o nó HTTP Request para `http://localhost:8000/atender`.

## Output de exemplo

API levantada em `127.0.0.1:8004`:

```bash
$ curl -s http://127.0.0.1:8004/health
{"status":"ok","provider":"mock"}

$ curl -s -X POST http://127.0.0.1:8004/atender \
    -H 'content-type: application/json' \
    -d '{"telefone":"+5511999990000","mensagem":"meu pedido nao chegou e ja faz 2 semanas"}'
{"intencao":"outro","resposta":"[mock-llm:e1d7568c] Resposta simulada ...","provider":"mock"}
```

> Sem `OPENAI_API_KEY`, o classificador de intenção cai em `outro` porque o `MockLLMClient` não responde com `saudacao/duvida/reclamacao`. Com chave real, o GPT classifica corretamente e a resposta sai personalizada por intenção.

Para testar com o n8n, importe `workflow.json` e ajuste a URL do nó HTTP Request para `http://host.docker.internal:8004/atender`.

## Entregáveis para portfólio
- API REST de atendimento + workflow n8n importável
- Demonstra integração no-code/low-code com IA
- Resposta contextual conforme intenção
