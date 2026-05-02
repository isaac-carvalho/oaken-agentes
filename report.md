# Cybersecurity Scan Report

**Data:** 2026-05-02
**Stack:** Python 3.11+ · FastAPI · LangChain/LangGraph · ChromaDB · scikit-learn · XGBoost · PyTorch · Streamlit · Terraform/AWS Lambda+Bedrock · Docker · Kubernetes/Helm · GitHub Pages
**Escopo:** monorepo `oaken-agentes` com 21 projetos práticos
**Contexto:** portfólio educacional (não produção) — severidade ajustada para esse contexto

## Sumário

| Severidade | Total | Resolvido |
|---|---|---|
| 🔴 CRÍTICO | 2 | ✅ **2** |
| 🟠 ALTO | 5 | ✅ **5** |
| 🟡 MÉDIO | 8 | ⚠️ **1 parcial** (MÉDIO-8 fix junto com ALTO-2) |
| 🟢 BAIXO | 6 | ⏳ pendente (sugestões) |
| **Total de achados** | **21** | **8 fixes aplicados** |

**Pontos fortes do projeto:**
- ✅ `.env` no `.gitignore` (e `.env.*` também)
- ✅ `.env.example` sem valores reais
- ✅ Nenhum secret hardcoded encontrado (varredura por padrões `sk-`, `AKIA`, `ghp_`, `eyJ`)
- ✅ Logs/print não imprimem secrets
- ✅ Dockerfile usa `USER oaken` (non-root)
- ✅ K8s tem `resources.requests/limits` definidos
- ✅ Guardrails LLM com PII redaction em 7 padrões + audit chain (projeto 10)
- ✅ Direito ao esquecimento implementado com cascade (projeto 12)
- ✅ Healthcheck no Dockerfile valida payload (`status=ok`)

---

## 🔴 Achados Críticos

> ✅ **Ambos os críticos foram resolvidos no commit `57bed0d`** com opt-in via `OAKEN_ALLOW_LOCAL_EXEC=1`. Default agora é seguro.

### [CRÍTICO-1] ✅ RESOLVIDO · Sandbox subprocess sem isolamento real
**Categoria:** 3 · CÓDIGO (Command injection / Insecure execution)
**Arquivo:** `projects/15-agente-codigo-sandbox/sandbox.py:11-22, 51`
**Impacto:** O fallback `_run_subprocess` executa código arbitrário gerado por LLM com `subprocess.run([sys.executable, "-c", code], ...)` no host. Tem timeout (10s) mas pode: ler `~/.ssh/`, `~/.aws/credentials`, vazar variáveis de ambiente, escrever em `/tmp`, fazer rede. Em prompt-injection, RCE imediato.
**Fix sugerido:**
1. Remover o fallback subprocess silencioso — exigir Docker presente.
2. Se manter, isolar com `firejail`/`bubblewrap` + namespace separado.
3. Adicionar aviso explícito no README: "uso apenas em ambiente descartável".

### [CRÍTICO-2] ✅ RESOLVIDO · Tool `python` do agente 07 executa código arbitrário do LLM
**Categoria:** 3 · CÓDIGO
**Arquivo:** `projects/07-agente-tools-zero-shot/main.py:54-65`
**Impacto:** Mesma classe do CRÍTICO-1 — `subprocess.run([sys.executable, "-c", code], timeout=10)` chamado pelo loop ReAct. LLM pode emitir `ACAO: {"tool":"python","input":"open('/etc/shadow').read()"}`. Se o agente for exposto via API web, comprometimento total.
**Fix sugerido:**
- Trocar tool `python` por execução em container Docker `network=none` (igual ao 15 com Docker presente).
- Whitelist de imports / modo restricted.
- Mover para um sub-agente que valida intenção antes de executar.

---

## 🟠 Achados Altos

> ✅ **Todos os 5 altos foram resolvidos.** Ver commits `57bed0d` (ALTO-1), `<commit-2>` (ALTO-2/3/4/5).

### [ALTO-1] ✅ RESOLVIDO · FastAPI sem CORS, rate limiting nem security headers
**Categoria:** 4 · INFRA
**Arquivos:** `projects/04-n8n-atendimento-whatsapp/api.py`, `projects/12-lgpd-compliance-toolkit/api.py`, `projects/21-deploy-docker-k8s/app.py`
**Impacto:** Comportamento default do FastAPI permite chamadas cross-origin de qualquer origem; sem `slowapi` qualquer cliente pode esgotar quota OpenAI/abrir DoS; sem CSP/HSTS/X-Frame-Options o recrutador que abrir o portfólio fica exposto a clickjacking se algum dia o app rodar em produção.
**Fix sugerido:**
```python
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(CORSMiddleware, allow_origins=["https://recuperarcontato4-prog.github.io"], allow_methods=["GET","POST"])

@app.middleware("http")
async def headers(req, call_next):
    resp = await call_next(req)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000"
    return resp
```

### [ALTO-2] ✅ RESOLVIDO · IAM Lambda com `logs:*` e `bedrock:InvokeModel` em `Resource = "*"`
**Categoria:** 5 · IAM
**Arquivo:** `projects/11-deploy-aws-bedrock/terraform/main.tf:33-37`
**Impacto:** Permissões mais amplas que o necessário. `logs:*` permite criar/destruir log groups arbitrários; `bedrock:InvokeModel` em `*` permite invocar qualquer modelo da conta (não só claude-haiku).
**Fix sugerido:**
```hcl
{ Effect = "Allow",
  Action = ["bedrock:InvokeModel"],
  Resource = "arn:aws:bedrock:${var.region}::foundation-model/anthropic.claude-haiku-4-5"
},
{ Effect = "Allow",
  Action = ["logs:CreateLogStream","logs:PutLogEvents"],
  Resource = "arn:aws:logs:${var.region}:*:log-group:/aws/lambda/oaken-chat:*"
}
```

### [ALTO-3] ✅ RESOLVIDO · Webhook n8n sem autenticação
**Categoria:** 4 · INFRA
**Arquivo:** `projects/04-n8n-atendimento-whatsapp/workflow.json` (nó `Webhook WhatsApp`)
**Impacto:** Webhook público sem `headerAuth`. Qualquer um pode invocar com payload arbitrário, gerando custo OpenAI e potencial spam para clientes.
**Fix sugerido:** No n8n, abrir o nó Webhook → **Authentication** → `Header Auth` → criar credencial com header `X-Webhook-Secret`.

### [ALTO-4] ✅ RESOLVIDO · Helm chart sem `securityContext`
**Categoria:** 4 · INFRA / 5 · IAM
**Arquivo:** `projects/21-deploy-docker-k8s/helm/templates/deployment.yaml`
**Impacto:** Sem `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, sem drop de capabilities. Em K8s real, container comprometido tem mais facilidade de escalar privilégios.
**Fix sugerido:** adicionar no spec do container:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: [ALL]
```

### [ALTO-5] ✅ RESOLVIDO · Helm `values.yaml` expõe API keys como env strings
**Categoria:** 1 · SECRETS
**Arquivo:** `projects/21-deploy-docker-k8s/helm/values.yaml:16-20`
**Impacto:** `env: OPENAI_API_KEY: ""` no `values.yaml` será materializado como string no Deployment YAML — visível em `kubectl describe pod` para qualquer um com read no namespace. Se commitarem o values com chave preenchida por engano, vaza no git.
**Fix sugerido:** Criar `Secret` separado e usar `envFrom`:
```yaml
# values.yaml
secrets:
  openaiApiKey: ""  # injetar via --set ou external-secrets

# templates/secret.yaml
apiVersion: v1
kind: Secret
metadata: { name: {{ .Release.Name }}-llm-keys }
type: Opaque
stringData:
  OPENAI_API_KEY: {{ .Values.secrets.openaiApiKey | quote }}

# deployment.yaml — container spec
envFrom:
  - secretRef: { name: {{ .Release.Name }}-llm-keys }
```

---

## 🟡 Achados Médios

### [MÉDIO-1] Sem validação de tamanho/formato em endpoints
**Categoria:** 3 · CÓDIGO
**Arquivos:** `projects/12-lgpd-compliance-toolkit/api.py:30-32, 94`, `projects/21-deploy-docker-k8s/app.py:18-19`
**Impacto:** `titular_id`, `texto`, `prompt` aceitam qualquer tamanho/charset. Texto de 100MB → DoS por consumo de memória.
**Fix:** Pydantic Field com `max_length`, `pattern`:
```python
class TextoIn(BaseModel):
    texto: str = Field(max_length=10000)
class Pergunta(BaseModel):
    prompt: str = Field(max_length=4000, min_length=1)
```

### [MÉDIO-2] Sem lock file de dependências
**Categoria:** 2 · DEPENDÊNCIAS
**Arquivos:** todos os `projects/**/requirements.txt`
**Impacto:** Versões em `>=` são pegas no momento do install — mesmo `pip install` em duas datas pode dar versões diferentes (incluindo CVEs introduzidos). Supply-chain attack mais difícil de detectar.
**Fix:** gerar `requirements.lock` via `pip-compile` (pip-tools) ou migrar para `uv` / `poetry`.

### [MÉDIO-3] Sem scan de CVEs no CI
**Categoria:** 2 · DEPENDÊNCIAS
**Arquivo:** `projects/21-deploy-docker-k8s/.github/workflows/ci.yml`
**Fix:** adicionar job `pip-audit` antes do build:
```yaml
- name: Audit deps
  run: |
    pip install pip-audit
    pip-audit -r projects/21-deploy-docker-k8s/requirements.txt
```

### [MÉDIO-4] `index.html` sem CSP meta-tag
**Categoria:** 4 · INFRA
**Arquivo:** `index.html`
**Fix:** adicionar no `<head>`:
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; style-src 'self' 'unsafe-inline' fonts.googleapis.com;
               font-src 'self' fonts.gstatic.com; img-src 'self' data:;">
```

### [MÉDIO-5] `pickle`/`joblib` é insecure deserialization
**Categoria:** 3 · CÓDIGO
**Arquivos:** `projects/16-ml-churn-shap/train.py` (`joblib.dump`), `projects/19-mlops-mlflow-dvc` (MLflow já avisa)
**Impacto:** Quem carregar um `modelo.pkl` malicioso é vítima de RCE. Risco crítico se modelos forem distribuídos publicamente; baixo se ficarem só no repo.
**Fix:** documentar no README que pickles **não** devem ser carregados de fontes não-confiáveis; opcionalmente migrar para `skops` (formato seguro para sklearn).

### [MÉDIO-6] Tool `web` do agente 07 sem timeout no DDGS
**Categoria:** 3 · CÓDIGO
**Arquivo:** `projects/07-agente-tools-zero-shot/main.py:47-49`
**Fix:** envolver com `concurrent.futures` + timeout, ou usar `requests` direto com `timeout=5`.

### [MÉDIO-7] Endpoint `/chat` (proj 21) sem autenticação
**Categoria:** 4 · INFRA / 5 · IAM
**Arquivo:** `projects/21-deploy-docker-k8s/app.py:41-44`
**Impacto:** Qualquer um chama → consome tokens OpenAI da sua chave. Custo financeiro real.
**Fix:** API key header obrigatória:
```python
from fastapi import Header, HTTPException
import os, secrets

API_KEY = os.environ.get("OAKEN_API_KEY")

@app.post("/chat")
def chat(p: Pergunta, x_api_key: str = Header(...)):
    if not API_KEY or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(401, "unauthorized")
    ...
```

### [MÉDIO-8] ✅ RESOLVIDO · Lambda vaza mensagem de erro do Bedrock para o cliente
**Categoria:** 3 · CÓDIGO
**Arquivo:** `projects/11-deploy-aws-bedrock/handler.py:30`
**Impacto:** `text = f"[mock-bedrock] eco: {message} (erro Bedrock: {exc})"` expõe `Unable to locate credentials` no body da resposta — vazamento de info de infraestrutura.
**Fix:** logar `exc` no CloudWatch e devolver mensagem genérica ao cliente.

---

## 🟢 Achados Baixos

### [BAIXO-1] GH Actions sem pin em SHA
**Categoria:** 2 · DEPENDÊNCIAS (supply-chain)
**Arquivo:** `projects/21-deploy-docker-k8s/.github/workflows/ci.yml`
**Atual:** `actions/checkout@v4`, `docker/login-action@v3`, `docker/build-push-action@v5`.
**Fix:** pin em SHA imutável (`actions/checkout@b4ffde6...`) — proteção contra repos comprometidos retroativamente.

### [BAIXO-2] Sem `.dockerignore`
**Categoria:** 4 · INFRA
**Arquivo:** `projects/21-deploy-docker-k8s/`
**Impacto:** `docker build .` pode acabar copiando `.git/`, `tests/`, `.venv/` se existir. Imagem maior + risco de copiar `.env` por engano.
**Fix:** criar `.dockerignore` com `.git`, `.venv`, `__pycache__`, `*.pyc`, `tests/`, `.env`.

### [BAIXO-3] Sem request ID / correlation no logging
**Categoria:** 7 · LOGS
**Impacto:** logs do FastAPI não incluem request ID — debugging em produção fica difícil.
**Fix:** middleware que gera `X-Request-Id` e injeta em `contextvars`.

### [BAIXO-4] Sem política de privacidade
**Categoria:** 6 · LGPD
**Impacto:** se um dia esses agentes forem expostos a usuários reais, falta texto formal de consentimento + bases legais.
**Fix:** template em `docs/PRIVACY.md` (não bloqueante para portfólio).

### [BAIXO-5] LGPD toolkit cobre apenas "esquecimento" — falta acesso e portabilidade
**Categoria:** 6 · LGPD
**Arquivo:** `projects/12-lgpd-compliance-toolkit/api.py`
**Fix:** adicionar `GET /titular/{id}/dados` (direito de acesso) e `GET /titular/{id}/export` (portabilidade — JSON/CSV).

### [BAIXO-6] BACKUP / DR
**Categoria:** 8 · BACKUP
**Status:** N/A para portfólio educacional (sem dados de produção). Se um dia subir LGPD toolkit em produção, configurar backup do `consent.json` + `audit_chain.log`.

---

## Por categoria — resumo

| Cat. | Tema | Achados | Cobertura |
|------|------|---------|-----------|
| 1 | SECRETS | 1 alto | ✅ exceto Helm values |
| 2 | DEPENDÊNCIAS | 2 médio + 1 baixo | ⚠️ falta lock + audit |
| 3 | CÓDIGO | 2 crítico + 4 médio | ⚠️ sandbox + validação |
| 4 | INFRA | 1 alto + 2 médio + 2 baixo | ⚠️ FastAPI middleware |
| 5 | IAM | 2 alto + 1 médio | ⚠️ least privilege |
| 6 | LGPD | 2 baixo | ✅ direitos parciais |
| 7 | LOGS | 1 baixo | ✅ audit chain |
| 8 | BACKUP | N/A | ✅ contexto |

## Próximos passos sugeridos

Ordem de prioridade para fix (impacto × esforço):
1. 🔴 **CRÍTICO-1 e CRÍTICO-2** — adicionar aviso explícito de "uso só local" ou exigir Docker (15 min)
2. 🟠 **ALTO-3** (n8n auth) e **ALTO-5** (Helm secrets) — fixes pequenos, alto impacto (30 min cada)
3. 🟠 **ALTO-1** (CORS + rate limit + headers) — middleware reusável que aplica nos 3 FastAPI (1h)
4. 🟠 **ALTO-2** (IAM least privilege) e **ALTO-4** (securityContext) — IaC (40 min)
5. 🟡 Médios em ordem do impacto

Quer que eu aplique algum desses fixes? Posso ir um por um:
- **(a)** Aplicar todos os CRÍTICOS de uma vez
- **(b)** Aplicar todos os ALTOS de uma vez
- **(c)** Pegar um específico (me diz qual número)
- **(d)** Aplicar tudo (CRÍTICO + ALTO + MÉDIO) num PR só

---

*Gerado por `/cybersecurity-scan` — 90 checks em 8 categorias.*
