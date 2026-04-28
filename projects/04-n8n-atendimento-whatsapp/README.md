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

## Entregáveis para portfólio
- API REST de atendimento + workflow n8n importável
- Demonstra integração no-code/low-code com IA
- Resposta contextual conforme intenção
