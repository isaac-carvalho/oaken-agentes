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

## Output de exemplo

Smoke test headless (sem subir Streamlit):

```bash
$ python -c "from app import build_clients, TASKS; \
    print('Clients:', list(build_clients())); \
    print('Tarefas:', list(TASKS))"
Clients: ['ollama/llama3.2', 'mock']
Tarefas: ['Resumir', 'Classificar sentimento', 'Gerar código']
```

Com `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY` exportadas, o `build_clients` adiciona `openai/gpt-4o-mini`, `gemini/flash`, `anthropic/haiku`. Subindo a UI:

```bash
$ streamlit run app.py
```

A UI exibe uma tabela `pandas` com colunas `modelo`, `latência_ms`, `erro`, `resposta` para cada modelo selecionado.

> Para incluir Llama local na comparação, instale e rode `ollama pull llama3.2` antes — o cliente faz `POST http://localhost:11434/api/generate`.

## Entregáveis para portfólio
- Comparativo objetivo entre LLMs
- Mostra capacidade de avaliação de modelos
- Inclui modelo open-source local (Ollama)
