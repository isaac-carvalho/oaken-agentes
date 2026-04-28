# 09 — Benchmark LLMs

> **Carreira Alura:** Especialista em IA — Nível 2 (*Comparação de modelos*)

Roda um conjunto de tarefas (resumo, classificação, código) em **vários modelos** lado a lado (incluindo Llama via **Ollama** local), exibe latência, custo e dump das respostas em uma tabela Streamlit.

## Stack
| Camada | Tecnologia |
|--------|------------|
| UI | `streamlit` |
| Modelos remotos | OpenAI, Gemini, Anthropic |
| Modelo local | `ollama` (ex: `llama3.2`) |
| Tabela | `pandas` |

## Como rodar

```bash
pip install -r requirements.txt
ollama pull llama3.2          # opcional, para benchmark local
streamlit run app.py
```

## Entregáveis para portfólio
- Comparativo objetivo entre LLMs
- Mostra capacidade de avaliação de modelos
- Inclui modelo open-source local (Ollama)
