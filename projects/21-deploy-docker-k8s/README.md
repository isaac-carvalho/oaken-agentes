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

## Entregáveis para portfólio
- Dockerfile profissional (multi-stage, non-root)
- Helm chart com values configuráveis (replicas, env, resources)
- Workflow GitHub Actions completo
- Healthcheck + readiness probe
