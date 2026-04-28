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

## Output de exemplo

### Handler em modo mock (sem AWS)
```bash
$ python -c "import json; from handler import lambda_handler; \
    print(lambda_handler({'body': json.dumps({'message':'olá'})}, None))"
{'statusCode': 200, 'headers': {...},
 'body': '{"reply":"[mock-bedrock] eco: olá (erro Bedrock: Unable to locate credentials)",
          "model":"anthropic.claude-haiku-4-5"}'}

$ python -c "from handler import lambda_handler; print(lambda_handler({'body':'{}'}, None))"
{'statusCode': 400, 'body': '{"error":"campo \\u0027message\\u0027 obrigat\\u00f3rio"}'}
```

Comportamento esperado: sem credenciais, o `boto3` falha localizando-as, o handler captura e devolve uma resposta `[mock-bedrock]` (200) — facilitando dev local. Validação de input continua funcionando (400 sem `message`).

### Terraform validado estruturalmente
```
8 resources: aws_iam_role, aws_iam_role_policy, aws_lambda_function,
             aws_apigatewayv2_api, _integration, _route, _stage,
             aws_lambda_permission
2 variables: region, model_id
1 output: api_url
```

Para deploy real:
```bash
cd terraform
terraform init && terraform apply -auto-approve
curl -X POST $(terraform output -raw api_url) -d '{"message":"oi"}'
```

> ⚠️ Pré-requisito: ter o modelo Bedrock habilitado na conta (Console → Bedrock → Model access → solicitar `anthropic.claude-haiku-4-5`).

## Entregáveis para portfólio
- IaC reproduzível (Terraform)
- Deploy serverless real
- Integração com Bedrock (Anthropic na AWS)
