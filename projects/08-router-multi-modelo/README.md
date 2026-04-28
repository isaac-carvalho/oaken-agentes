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

## Entregáveis para portfólio
- Política declarativa de roteamento
- Fallback resiliente
- Métricas por requisição (provider escolhido, motivo, custo)
