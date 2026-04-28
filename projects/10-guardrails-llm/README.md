# 10 — Guardrails para LLMs

> **Carreira Alura:** Especialista em IA — Nível 3 (*Governança*)

Wrapper que aplica **proteções obrigatórias** antes/depois de chamar um LLM:
1. **PII redaction** no input (CPF, email, telefone) via regex (Presidio opcional)
2. **Filtro de toxicidade** no output (heurística leve, expansível para Detoxify)
3. **Audit log** estruturado (JSON Lines) com hash do prompt

## Stack
| Camada | Tecnologia |
|--------|------------|
| Detecção PII | regex / `presidio-analyzer` (opcional) |
| Toxicidade | lista de termos bloqueados (heurística) |
| Logs | JSON Lines |

## Como rodar

```bash
pip install -r requirements.txt
python main.py "Meu CPF é 123.456.789-00 e quero ajuda"
cat audit.log
```

## Entregáveis para portfólio
- Padrão de segurança aplicável a qualquer chamada LLM
- Demonstra preocupação com governança (LGPD, segurança)
- Audit log auditável (hash + timestamp)
