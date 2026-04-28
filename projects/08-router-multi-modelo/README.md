# 08 — Router Multi-Modelo

> **Carreira Alura:** Especialista em IA — Nível 2 (*Modelos*)

Roteador inteligente que escolhe entre **OpenAI / Gemini / Anthropic** baseado em regras simples (custo, latência alvo, complexidade da tarefa). Inclui fallback automático em caso de falha.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Roteamento | regras Pydantic |
| Providers | `openai`, `google-generativeai`, `anthropic` |

## Como rodar

```bash
pip install -r requirements.txt
python main.py "tarefa simples: classifique como spam ou ham"
python main.py --task complex "explique mecânica quântica para um doutorando"
python main.py --max-cost 0.001 "resumo curto"
```

Configuração em `policies.yaml`.

## Output de exemplo

A política em `policies.yaml` decide o modelo conforme `task` e `max_cost`. Validado com 3 cenários:

```bash
# task simples, orçamento apertado → escolhe o mais barato (Gemini Flash)
$ python main.py "classifique como spam: ..." --task simple --max-cost 0.0005
[router] escolhido: gemini-1.5-flash (gemini) — custo estimado ~$0.00006

# task complexa, orçamento generoso → escolhe o melhor (Claude Sonnet)
$ python main.py "explique mecânica quântica..." --task complex --max-cost 0.05
[router] escolhido: claude-sonnet-4-6 (anthropic) — custo estimado ~$0.00303

# orçamento absurdamente baixo → fallback para o mais barato disponível
$ python main.py "resumo curto" --task simple --max-cost 0.000001
[router] escolhido: gemini-1.5-flash (gemini) — custo estimado ~$0.00006
```

Sem API key, depois de escolher o modelo o router cai no `MockLLMClient` (`[router] sem API key — usando MockLLMClient`). Com chave configurada do provedor escolhido, a resposta vem de fato dele.

## Entregáveis para portfólio
- Política declarativa de roteamento
- Fallback resiliente
- Métricas por requisição (provider escolhido, motivo, custo)
