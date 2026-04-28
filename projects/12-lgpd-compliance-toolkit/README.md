# 12 — Toolkit de Compliance LGPD

> **Carreira Alura:** Especialista em IA — Nível 3 (*Governança e LGPD*)

API + biblioteca para apoiar conformidade **LGPD** em sistemas de IA: anonimização de dados pessoais, gestão de consentimento por finalidade, e log auditável imutável (append-only com hash chain).

## Stack
| Camada | Tecnologia |
|--------|------------|
| API | FastAPI |
| PII | regex (Presidio opcional) |
| Hash chain | SHA-256 |

## Como rodar

```bash
pip install -r requirements.txt
uvicorn api:app --reload
# anonimizar
curl -X POST localhost:8000/anonimizar -H 'content-type: application/json' \
  -d '{"texto":"João, CPF 123.456.789-00, mora em SP"}'
# registrar consentimento
curl -X POST localhost:8000/consentimento -H 'content-type: application/json' \
  -d '{"titular":"abc-123","finalidade":"marketing","aceito":true}'
# auditoria
curl localhost:8000/auditoria
```

## Entregáveis para portfólio
- Compliance pragmático (não só docs)
- Hash chain demonstra preocupação com integridade
- Endpoint para exportar/excluir dados (direitos do titular)
