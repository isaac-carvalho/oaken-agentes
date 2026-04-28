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

## Output de exemplo

PII redaction + audit log:
```bash
$ python main.py "Meu CPF é 123.456.789-00, email joao@email.com, telefone (11) 91234-5678 — quero ajuda"
Redactions aplicadas: {'cpf': 1, 'email': 1, 'phone': 1}
✅ Resposta: [mock-llm:be594612] Resposta simulada ...
```

Bloqueio por toxicidade (input descartado antes de chegar ao LLM):
```bash
$ python main.py "como matar uma planta?"
Redactions aplicadas: nenhuma
❌ BLOQUEADO: contém termo bloqueado: matar
```

`audit.log` (JSON Lines):
```json
{"event":"completion","hash":"619699a1535e70de","provider":"mock","redactions":{"cpf":1,"email":1,"phone":1},"out_blocked":false,"ts":"2026-04-28T09:26:42.848188+00:00"}
{"event":"blocked_input","hash":"0bd59207aa53cdd3","reason":"contém termo bloqueado: matar","ts":"2026-04-28T09:26:42.921900+00:00"}
```

## Entregáveis para portfólio
- Padrão de segurança aplicável a qualquer chamada LLM
- Demonstra preocupação com governança (LGPD, segurança)
- Audit log auditável (hash + timestamp)
