# `_shared/` — utilitários comuns

Reutilizado pelos 21 projetos do portfólio.

- `env.py` — carrega `.env` automaticamente subindo até a raiz do repo
- `llm_clients.py` — wrappers para OpenAI, Gemini e Anthropic com fallback `MockLLMClient` (smoke tests sem internet)

```python
from projects._shared import get_default_client
client = get_default_client()         # auto-detecta API keys
print(client.complete("Olá, mundo!").text)
```
