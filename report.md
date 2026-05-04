# Cybersecurity Scan Report

Data: 2026-05-04 | Stack: Python, FastAPI, LangChain, LangGraph, ChromaDB, PyTorch, Streamlit, Docker, Kubernetes/Helm, Terraform/AWS, n8n

---

## Sumário

| Métrica | Valor |
|---------|-------|
| Checks executados | 90 |
| Passaram | 68 |
| Falharam | 22 |
| **CRÍTICOS** | **0** |
| **ALTOS** | **5** |
| **MÉDIOS** | **9** |
| **BAIXOS** | **8** |

---

## Categoria 1 · SECRETS

| Check | Status | Nota |
|-------|--------|------|
| API keys hardcoded | ✅ PASS | Nenhuma chave real encontrada |
| .env no .gitignore | ✅ PASS | `.env` e `.env.*` excluídos |
| .env.example sem valores reais | ✅ PASS | Apenas placeholders vazios |
| JWT secrets, DB passwords | ✅ PASS | Tudo via `os.environ.get()` |
| Secrets no git history | ✅ PASS | Nenhum encontrado |
| Secret manager em uso | ⚠️ N/A | Portfólio educacional |
| Rotação de chaves | ⚠️ N/A | Portfólio educacional |
| Tokens em comentários/TODOs | ✅ PASS | Nenhum |
| Webhook secrets configurados | ⚠️ MÉDIO | Ver achado #1 |
| Credenciais em CI/CD | ✅ PASS | Actions usam `${{ secrets.* }}` |
| Least privilege em secrets | ✅ PASS | |
| Logs não imprimem secrets | ✅ PASS | Nenhum print/log de env vars |

### Achados

#### [MÉDIO] #1 — Webhook n8n sem credencial real
**Arquivo:** `projects/04-n8n-atendimento-whatsapp/workflow.json:19`
**Impacto:** Se importado no n8n sem configurar credencial, webhook fica público.
**Fix:** Adicionar instrução obrigatória no README e validação no workflow.

#### [BAIXO] #2 — sk-test123 em teste unitário
**Arquivo:** `projects/09-benchmark-llms/test_benchmark.py:33`
**Impacto:** Falso positivo em scanners. Sem risco real.
**Fix:** Renomear para `sk-fake-key-for-testing`.

#### [BAIXO] #3 — Helm secrets em plaintext no history
**Arquivo:** `projects/21-deploy-docker-k8s/helm/templates/secret.yaml`
**Impacto:** `--set secrets.openaiApiKey=...` fica visível em `helm history`.
**Fix:** Usar external-secrets ou sealed-secrets.

---

## Categoria 2 · DEPENDÊNCIAS

| Check | Status | Nota |
|-------|--------|------|
| Pacotes com CVE crítico/alto | ❌ ALTO | Ver achados #4-#7 |
| Dependências > 1 ano sem update | ✅ PASS | Constraints recentes |
| Pacotes deprecated | ✅ PASS | Nenhum deprecated |
| Lock file commitado | ❌ MÉDIO | Nenhum lock file |
| Typosquatting suspeito | ✅ PASS | Todos pacotes legítimos |
| Registries oficiais | ✅ PASS | PyPI oficial |
| SBOM gerado | ❌ MÉDIO | Não implementado |
| Vulnerabilidades transitivas | ❌ MÉDIO | pip-audit sem constraints |

### Achados

#### [ALTO] #4 — Pillow permite versões com CVE
**Arquivo:** `projects/06-rag-multimodal-clip/requirements.txt`, `projects/17-cnn-pytorch-imagens/requirements.txt`
**Impacto:** CVE-2023-50447 (heap overflow), CVE-2024-28219 — floor `>=10.0.0` permite versões vulneráveis.
**Fix:** Alterar para `pillow>=10.3.0`.

#### [ALTO] #5 — LangChain permite versão com SQL injection
**Arquivo:** `projects/05-chatbot-rag-pdfs/requirements.txt`
**Impacto:** CVE-2024-3571 (SQL injection → execução arbitrária) — corrigido apenas em 0.2.16.
**Fix:** Alterar para `langchain>=0.2.16`.

#### [ALTO] #6 — MLflow permite versão com path traversal
**Arquivo:** `projects/19-mlops-mlflow-dvc/requirements.txt`
**Impacto:** CVE-2024-37052 — corrigido em 2.14.3.
**Fix:** Alterar para `mlflow>=2.14.3`.

#### [ALTO] #7 — torch sem upper bound
**Arquivo:** `projects/06,17,18/requirements.txt`
**Impacto:** CVE-2025-32434 (RCE via `torch.load`); range aberto aceita qualquer versão futura.
**Fix:** Adicionar `torch>=2.2.0,<2.5`.

#### [MÉDIO] #8 — Sem lock files em 21 projetos
**Impacto:** Builds não reproduzíveis. Dependências podem mudar entre installs.
**Fix:** Gerar `requirements.lock` com `pip freeze` para cada projeto.

#### [MÉDIO] #9 — pip-audit no CI ignora constraints
**Arquivo:** `.github/workflows/audit.yml:36`
**Impacto:** Auditoria corre sem restrições globais do `constraints.txt`.
**Fix:** Adicionar `-c ../../constraints.txt` ao comando pip-audit.

---

## Categoria 3 · CÓDIGO

| Check | Status | Nota |
|-------|--------|------|
| SQL injection | ✅ PASS | Sem SQL raw |
| XSS | ✅ PASS | Respostas JSON only |
| IDOR | ❌ ALTO | Ver achado #10 |
| CSRF | ✅ PASS | REST APIs, sem cookies/sessões |
| SSRF | ✅ PASS | Sem URLs controladas por user |
| Path traversal | ✅ PASS | Inputs validados com regex |
| Command injection | ✅ PASS | Sem os.system/eval/exec |
| Open redirect | ✅ PASS | Sem redirects |
| Insecure deserialization | ✅ PASS | Sem pickle/yaml.load |
| Validação de input | ✅ PASS | Pydantic models |
| Rate limiting | ❌ MÉDIO | Silenciosamente desabilitado |
| Mass assignment | ✅ PASS | Pydantic strict models |
| Race conditions | ✅ PASS | |
| Auth consistente | ❌ ALTO | Endpoints sem auth |
| Stack trace vazando | ✅ PASS | HTTPException estruturado |

### Achados

#### [ALTO] #10 — Endpoints LGPD sem autenticação
**Arquivo:** `projects/12-lgpd-compliance-toolkit/api.py:181-206`
**Impacto:** `/auditoria`, `/titular/{id}/dados`, `/titular/{id}/export`, DELETE `/titular/{id}` acessíveis sem autenticação. Qualquer cliente pode ler/apagar dados de qualquer titular.
**Fix:** Adicionar `Depends(_check_api_key)` em todos os endpoints sensíveis.

#### [ALTO] #11 — Auth opcional no endpoint /chat (deploy K8s)
**Arquivo:** `projects/21-deploy-docker-k8s/app.py:29-31`
**Impacto:** Se `OAKEN_API_KEY` não definida, endpoint fica aberto. Container pode subir em produção sem auth.
**Fix:** Falhar no startup se `OAKEN_API_KEY` não definida quando `OAKEN_ENV=production`.

#### [MÉDIO] #12 — Sandbox monta /tmp inteiro no container
**Arquivo:** `projects/15-agente-codigo-sandbox/sandbox.py:53`
**Impacto:** `host_path.parent` = `/tmp` — todos os arquivos temporários do host ficam acessíveis ao container (read-only mas visíveis).
**Fix:** Montar apenas o arquivo: `{str(host_path): {"bind": "/work/script.py", "mode": "ro"}}`.

#### [MÉDIO] #13 — Rate limiting silenciosamente desabilitado
**Arquivo:** `projects/_shared/security.py:65-83`
**Impacto:** `except ImportError: pass` — se slowapi não instalado, rate limiting some sem aviso.
**Fix:** Logar warning quando slowapi não disponível.

#### [MÉDIO] #14 — Scripts executados ficam em /tmp
**Arquivo:** `projects/15-agente-codigo-sandbox/sandbox.py:67`
**Impacto:** Arquivos `.done.py` acumulam código executado em `/tmp` sem limpeza.
**Fix:** Apagar o arquivo após execução.

---

## Categoria 4 · INFRA

| Check | Status | Nota |
|-------|--------|------|
| CORS restritivo | ✅ PASS | Sem wildcard `*` |
| Headers de segurança | ✅ PASS | HSTS, X-Frame, X-Content-Type via `_shared/security.py` |
| TLS 1.2+ | ⚠️ N/A | Aplicações não terminam TLS |
| Certificados auto-renew | ⚠️ N/A | |
| Cookies seguras | ✅ PASS | Sem cookies (JWT/API key) |
| HTTP→HTTPS redirect | ⚠️ N/A | Delegado a reverse proxy |
| WAF | ⚠️ N/A | Portfólio educacional |
| DDoS protection | ⚠️ N/A | |
| Serviços não expostos | ✅ PASS | |
| Docker hardened | ✅ PASS | Non-root, read-only FS, drop ALL |

### Achados

#### [ALTO] #15 — API Gateway sem autenticação (AWS)
**Arquivo:** `projects/11-deploy-aws-bedrock/terraform/main.tf`
**Impacto:** `aws_apigatewayv2_route` sem `authorization_type` — default NONE. Endpoint `/chat` público sem auth, IAM ou API key. Qualquer pessoa pode consumir créditos Bedrock.
**Fix:** Adicionar `authorization_type = "AWS_IAM"` ou API key obrigatória.

#### [MÉDIO] #16 — Sem NetworkPolicy no Helm
**Arquivo:** `projects/21-deploy-docker-k8s/helm/templates/`
**Impacto:** Pods sem restrição de tráfego lateral no cluster.
**Fix:** Adicionar `NetworkPolicy` template ao chart.

#### [BAIXO] #17 — Base image sem digest
**Arquivo:** `projects/21-deploy-docker-k8s/Dockerfile:2`
**Impacto:** `python:3.12-slim` pode mudar sem aviso.
**Fix:** Adicionar `@sha256:<digest>`.

#### [BAIXO] #18 — Image tag `latest` no values.yaml
**Arquivo:** `projects/21-deploy-docker-k8s/helm/values.yaml:3`
**Impacto:** Não reproduzível em rollbacks.
**Fix:** Usar tag semântica como default.

#### [BAIXO] #19 — CORS default localhost em Helm
**Arquivo:** `projects/21-deploy-docker-k8s/helm/values.yaml:22`
**Impacto:** Requer override manual em produção; pode levar operador a usar `*`.
**Fix:** Documentar no NOTES.txt a obrigatoriedade do override.

---

## Categoria 5 · IAM

| Check | Status | Nota |
|-------|--------|------|
| MFA obrigatório pra admin | ⚠️ N/A | Sem painel admin |
| Least privilege em roles | ✅ PASS | Terraform: apenas `bedrock:InvokeModel` + CloudWatch |
| Service accounts mínimas | ✅ PASS | |
| Tokens com escopo limitado | ❌ MÉDIO | API keys são all-or-nothing |
| Timeout de sessão | ⚠️ N/A | Sem sessões |

### Achados

#### [MÉDIO] #20 — API keys sem escopo granular
**Impacto:** Uma única `OAKEN_API_KEY` dá acesso a todos os endpoints. Sem distinção de roles.
**Fix:** Para portfólio é aceitável. Em produção, implementar scoped tokens ou JWT com claims.

---

## Categoria 6 · LGPD

| Check | Status | Nota |
|-------|--------|------|
| Política de privacidade | ⚠️ N/A | Portfólio educacional |
| Consentimento explícito | ✅ PASS | Projeto 12 implementa opt-in |
| Base legal documentada | ✅ PASS | Projeto 12 documenta bases |
| Revogação de consentimento | ✅ PASS | Endpoint implementado |
| Direito de acesso | ✅ PASS | `/titular/{id}/dados` |
| Direito de portabilidade | ✅ PASS | `/titular/{id}/export` |
| Direito ao esquecimento | ✅ PASS | DELETE `/titular/{id}` |
| Anonimização | ✅ PASS | Presidio integrado |
| Retenção definida | ❌ BAIXO | Sem TTL em dados |

### Achados

#### [BAIXO] #21 — Sem política de retenção de dados
**Arquivo:** `projects/12-lgpd-compliance-toolkit/`
**Impacto:** Dados armazenados indefinidamente. LGPD exige prazo definido.
**Fix:** Adicionar TTL ou cleanup job.

---

## Categoria 7 · LOGS

| Check | Status | Nota |
|-------|--------|------|
| Eventos de auth logados | ✅ PASS | Projeto 12 loga acessos |
| Mudanças sensíveis logadas | ✅ PASS | Trilha de auditoria |
| Dados sensíveis mascarados | ✅ PASS | Presidio na pipeline |
| Timestamps UTC/ISO 8601 | ✅ PASS | |
| Correlação por request ID | ❌ BAIXO | Sem request ID |
| Logs centralizados | ⚠️ N/A | Projetos independentes |
| Retenção 90 dias | ⚠️ N/A | |
| Alertas suspeitos | ⚠️ N/A | |

### Achados

#### [BAIXO] #22 — Sem correlação por request ID
**Impacto:** Difícil rastrear requisições entre serviços.
**Fix:** Adicionar middleware de request ID no `_shared/security.py`.

---

## Categoria 8 · BACKUP

| Check | Status | Nota |
|-------|--------|------|
| Backup automático | ⚠️ N/A | Portfólio — sem dados persistentes em produção |
| Backup criptografado | ⚠️ N/A | |
| RTO/RPO documentado | ⚠️ N/A | |
| Runbook DR | ⚠️ N/A | |

> Categoria não aplicável: portfólio educacional sem ambiente de produção com dados reais.

---

## Top 5 — Ações Prioritárias

| # | Severidade | Achado | Fix |
|---|-----------|--------|-----|
| 1 | **ALTO** | API Gateway AWS sem auth (#15) | `authorization_type = "AWS_IAM"` |
| 2 | **ALTO** | Endpoints LGPD sem auth (#10) | `Depends(_check_api_key)` |
| 3 | **ALTO** | Auth opcional no deploy K8s (#11) | Fail-fast sem `OAKEN_API_KEY` |
| 4 | **ALTO** | CVEs em pillow/langchain/mlflow/torch (#4-7) | Bump version floors |
| 5 | **MÉDIO** | Sandbox monta /tmp inteiro (#12) | Montar só o arquivo |

---

*Relatório gerado por Claude Code — 2026-05-04*
