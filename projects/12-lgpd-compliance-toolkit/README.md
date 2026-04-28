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

## Output de exemplo

API de pé em `:8012`. Anonimização redireciona 3 PIIs e devolve hash:
```bash
$ curl -s -X POST :8012/anonimizar -H 'content-type: application/json' \
    -d '{"texto":"Joao Silva, CPF 123.456.789-00, email joao@test.com, RG 12.345.678-9"}'
{"texto":"Joao Silva, CPF [CPF], email [EMAIL], RG [RG]",
 "encontrados":{"cpf":1,"email":1,"rg":1},
 "audit_hash":"cd3a1ca7bcea1820efd386d371f26e1a89e3f230aa83f8bec638b1ec77ff801e"}
```

Hash chain auditável (cada registro encadeia o anterior via SHA-256):
```bash
$ curl -s :8012/auditoria/verificar
{"valido":true,"n":3}
```

Direito ao esquecimento (LGPD art. 18):
```bash
$ curl -s -X DELETE :8012/titular/abc-123
{"removido":true,"audit_hash":"ad4ed6af2966163d32ad06a243c2afe4aa39cd546b0bea5d43356c088ea4cd6e"}
```

Endpoints validados ponta a ponta: `POST /anonimizar`, `POST /consentimento`, `DELETE /titular/{id}`, `GET /auditoria`, `GET /auditoria/verificar`.

## Entregáveis para portfólio
- Compliance pragmático (não só docs)
- Hash chain demonstra preocupação com integridade
- Endpoint para exportar/excluir dados (direitos do titular)
