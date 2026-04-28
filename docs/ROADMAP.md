# Roadmap — Portfólio Oaken Agentes

Ordem sugerida de execução, mapeada às carreiras Alura.

## Sequência recomendada

1. **Fundamentos (01–03)** — destravam os demais. Estabelece o cliente LLM compartilhado.
2. **Especialista em IA — Nível 1 (04–06)** — RAG e chatbots; entrega visual rápida (bom para LinkedIn).
3. **Especialista em IA — Nível 2 (07–09)** — Agentes & comparação de modelos.
4. **Especialista em IA — Nível 3 (10–12)** — Governança, cloud e LGPD; áreas que muita gente ignora e diferenciam o portfólio.
5. **Engenharia de Agentes — Nível 1 (13–15)** — Agentes mais sofisticados (LangGraph, multi-agente, sandbox).
6. **Engenharia de Agentes — Nível 2 (16–18)** — ML supervisionado, deep learning, fine-tuning.
7. **Engenharia de Agentes — Nível 3 (19–21)** — Operação: MLOps, AIOps, deploy K8s.

## Mapeamento por checkpoint Alura

### Especialista em IA
| Checkpoint Alura | Projetos |
|-----------------|----------|
| Base (Python + APIs LLM) | 01, 02 |
| N1 — N8N, Chatbots e RAG | 04, 05, 06 |
| N2 — Agentes e modelos | 07, 08, 09 |
| N3 — Governança e Cloud | 10, 11, 12 |

### Engenharia de Agentes de IA
| Checkpoint Alura | Projetos |
|-----------------|----------|
| Base (Python + APIs LLM) | 01, 02 |
| N1 — Agentes Inteligentes com RAG | 13, 14, 15 |
| N2 — ML, DL, Fine Tuning | 16, 17, 18 |
| N3 — MLOps e AIOps | 19, 20, 21 |

O projeto **03** (eval de prompts) é transversal: serve em ambas as carreiras.

## Skills demonstradas (para CV / LinkedIn)

- **Python**: 21/21 projetos
- **LangChain / LangGraph**: 05, 07, 13, 14, 15
- **RAG (vector stores, embeddings)**: 05, 06, 13
- **Multi-agentes**: 14
- **n8n / automação no-code**: 04
- **FastAPI / APIs REST**: 04, 12, 21
- **Streamlit / dashboards**: 05, 09, 16
- **Machine Learning supervisionado + interpretabilidade**: 16
- **Deep Learning (PyTorch, transfer learning)**: 17
- **Fine-tuning LLM (LoRA + quantização)**: 18
- **MLOps (MLflow, DVC)**: 19
- **AIOps / observabilidade (Langfuse)**: 20
- **Cloud (AWS Bedrock + Terraform)**: 11
- **Containers + Kubernetes + Helm**: 21
- **CI/CD (GitHub Actions)**: 21
- **Governança / LGPD / segurança**: 10, 12

## Dicas para apresentar no portfólio

- O **portal `index.html`** é o link único para colar no LinkedIn / CV.
- Em cada projeto, o `README.md` tem um padrão fixo: recrutador rápido entende em 30 segundos.
- Para entrevistas, escolha 3-4 projetos da sua zona de força para discutir em profundidade.
- O `_shared/llm_clients.py` com fallback `MockLLMClient` mostra **maturidade técnica** (resilência, testabilidade) — vale puxar isso em conversas.
