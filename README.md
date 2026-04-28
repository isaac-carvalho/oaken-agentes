# Oaken Agentes — Portfólio de IA & Agentes

> 21 projetos práticos cobrindo as carreiras **Especialista em IA** e **Engenharia de Agentes de IA** (Alura).
> Pensado para demonstrar, em poucos minutos, capacidade técnica ponta-a-ponta: do primeiro script Python até deploy de agentes em Kubernetes.

**Portal visual:** abra [`index.html`](./index.html) no navegador — ou veja o [roadmap](./docs/ROADMAP.md).
**Landing original do produto Oaken IA:** [`pito-presentation.html`](./pito-presentation.html).

---

## Como navegar

```
projects/
├── _shared/                      # utils reaproveitados (clientes LLM, .env loader)
├── 01-python-api-llm-helper/     # Fundamentos
├── 02-pandas-ia-analista/
├── 03-eval-prompts-framework/
├── 04-12 ...                     # Trilha Especialista em IA
└── 13-21 ...                     # Trilha Engenharia de Agentes de IA
```

Cada pasta tem o mesmo padrão: `README.md` (objetivo, stack, como rodar), `requirements.txt`, `.env.example` quando preciso, e um `main.py` (ou equivalente) rodável.

## Os 21 projetos

### Fundamentos — base compartilhada
| # | Projeto | Stack-chave |
|---|---------|-------------|
| 01 | [python-api-llm-helper](./projects/01-python-api-llm-helper/) | OpenAI, Gemini, Typer |
| 02 | [pandas-ia-analista](./projects/02-pandas-ia-analista/) | Pandas, Matplotlib, LLM |
| 03 | [eval-prompts-framework](./projects/03-eval-prompts-framework/) | Pydantic, OpenAI, pytest |

### Especialista em IA
| # | Projeto | Stack-chave |
|---|---------|-------------|
| 04 | [n8n-atendimento-whatsapp](./projects/04-n8n-atendimento-whatsapp/) | n8n, FastAPI |
| 05 | [chatbot-rag-pdfs](./projects/05-chatbot-rag-pdfs/) | Streamlit, LangChain, ChromaDB |
| 06 | [rag-multimodal-clip](./projects/06-rag-multimodal-clip/) | CLIP, ChromaDB |
| 07 | [agente-tools-zero-shot](./projects/07-agente-tools-zero-shot/) | LangChain, DuckDuckGo |
| 08 | [router-multi-modelo](./projects/08-router-multi-modelo/) | LiteLLM, Pydantic |
| 09 | [benchmark-llms](./projects/09-benchmark-llms/) | Ollama, Pandas, Streamlit |
| 10 | [guardrails-llm](./projects/10-guardrails-llm/) | Presidio, Detoxify |
| 11 | [deploy-aws-bedrock](./projects/11-deploy-aws-bedrock/) | boto3, Terraform, Bedrock |
| 12 | [lgpd-compliance-toolkit](./projects/12-lgpd-compliance-toolkit/) | Presidio, FastAPI |

### Engenharia de Agentes de IA
| # | Projeto | Stack-chave |
|---|---------|-------------|
| 13 | [agente-rag-langgraph](./projects/13-agente-rag-langgraph/) | LangGraph, ChromaDB |
| 14 | [multi-agente-pesquisa](./projects/14-multi-agente-pesquisa/) | LangGraph, CrewAI |
| 15 | [agente-codigo-sandbox](./projects/15-agente-codigo-sandbox/) | LangGraph, Docker |
| 16 | [ml-churn-shap](./projects/16-ml-churn-shap/) | XGBoost, SHAP, Streamlit |
| 17 | [cnn-pytorch-imagens](./projects/17-cnn-pytorch-imagens/) | PyTorch, torchvision |
| 18 | [fine-tuning-lora](./projects/18-fine-tuning-lora/) | Transformers, PEFT |
| 19 | [mlops-mlflow-dvc](./projects/19-mlops-mlflow-dvc/) | MLflow, DVC |
| 20 | [aiops-langfuse](./projects/20-aiops-langfuse/) | Langfuse, LangChain |
| 21 | [deploy-docker-k8s](./projects/21-deploy-docker-k8s/) | Docker, Kubernetes, Helm |

## Setup rápido

```bash
git clone https://github.com/recuperarcontato4-prog/oaken-agentes
cd oaken-agentes
cp projects/.env.example projects/.env   # edite com suas chaves
python -m venv .venv && source .venv/bin/activate
# em cada projeto: pip install -r projects/<nome>/requirements.txt
```

Sem API keys? Os projetos que dependem de LLM caem para um `MockLLMClient` determinístico (em `projects/_shared/llm_clients.py`), garantindo que o smoke test rode offline.

## Carreiras Alura cobertas

- **Especialista em IA** — fundamentos Python+LLMs, n8n, Chatbots, RAG, Agentes & Modelos, Governança & Cloud
- **Engenharia de Agentes de IA** — RAG avançado, ML/DL/Fine Tuning, MLOps & AIOps

Mapeamento detalhado por nível e checkpoint em [`docs/ROADMAP.md`](./docs/ROADMAP.md).

## Licença

[MIT](./LICENSE)
