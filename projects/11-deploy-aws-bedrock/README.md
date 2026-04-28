# 11 — Deploy serverless: AWS Lambda + Bedrock

> **Carreira Alura:** Especialista em IA — Nível 3 (*Cloud*)

Chatbot serverless completo: **API Gateway → Lambda (Python) → Bedrock (Claude)**, infraestrutura como código com **Terraform**.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Compute | AWS Lambda (Python 3.12) |
| Modelo | AWS Bedrock — `anthropic.claude-haiku-4-5` |
| Edge | API Gateway REST |
| IaC | Terraform |

## Como rodar (deploy real)

Pré-requisitos: AWS CLI configurado, modelo Bedrock habilitado na conta, Terraform >= 1.6.

```bash
cd terraform/
terraform init
terraform apply
# anote o output api_url
curl -X POST $API_URL -d '{"message":"oi"}'
```

Deploy local sem AWS: rode o handler diretamente.
```bash
pip install -r requirements.txt
python -c "from handler import lambda_handler; print(lambda_handler({'body': '{\"message\":\"oi\"}'}, None))"
```

## Entregáveis para portfólio
- IaC reproduzível (Terraform)
- Deploy serverless real
- Integração com Bedrock (Anthropic na AWS)
