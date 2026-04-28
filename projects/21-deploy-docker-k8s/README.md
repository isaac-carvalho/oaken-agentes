# 21 — Deploy de Agente em Docker + Kubernetes

> **Carreira Alura:** Engenharia de Agentes — Nível 3 (*Operação em Produção*)

Empacotamento end-to-end de um agente: **FastAPI** → **Dockerfile** multi-stage → **Helm chart** Kubernetes → **GitHub Actions** (build & push).

## Stack
| Camada | Tecnologia |
|--------|------------|
| App | FastAPI |
| Container | Docker (multi-stage) |
| Orquestração | Kubernetes + Helm |
| CI/CD | GitHub Actions |

## Como rodar

```bash
pip install -r requirements.txt
uvicorn app:app --reload                     # local

docker build -t oaken-agent:dev .
docker run -p 8000:8000 oaken-agent:dev      # container

helm install agent ./helm                    # k8s (kind/minikube ou cluster real)
kubectl port-forward svc/agent 8000:80
```

CI: `.github/workflows/ci.yml` constrói a imagem e publica em GHCR a cada push em `main`.

## Output de exemplo

App levantado localmente (`uvicorn app:app --port 8021`):

```bash
$ curl -s :8021/health
{"status":"ok"}

$ curl -s :8021/ready
{"status":"ready","provider":"mock"}

$ curl -s -X POST :8021/chat -H 'content-type: application/json' -d '{"prompt":"oi"}'
{"reply":"[mock-llm:82e8e83b] Resposta simulada ...","provider":"mock","model":"mock-1"}
```

Estrutura validada estaticamente (sem precisar de docker/helm instalados):

| Arquivo | Check |
|---------|-------|
| `Dockerfile` | multi-stage, non-root user, healthcheck, sem caminhos `../` |
| `helm/Chart.yaml` | `apiVersion: v2`, `name: oaken-agent`, `type: application` |
| `helm/values.yaml` | `image`, `replicaCount`, `service`, `resources` |
| `helm/templates/deployment.yaml` | `Deployment`, `replicas`, `readinessProbe`, `livenessProbe` |
| `helm/templates/service.yaml` | `Service`, `ports`, `selector` |
| `.github/workflows/ci.yml` | YAML válido, build+push para GHCR |

> **Decisão de design**: o projeto 21 é **self-contained** (inclui sua própria cópia de `_shared/`) para que `docker build .` funcione sem mudar o build context do monorepo. Isso causa duplicação de ~120 linhas — trade-off consciente.

## Entregáveis para portfólio
- Dockerfile profissional (multi-stage, non-root)
- Helm chart com values configuráveis (replicas, env, resources)
- Workflow GitHub Actions completo
- Healthcheck + readiness probe
