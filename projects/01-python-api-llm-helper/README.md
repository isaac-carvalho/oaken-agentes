# 01 — Python API LLM Helper

> **Carreira Alura:** Base — *Python: Inteligência Artificial Aplicada*

CLI em Python que recebe uma tarefa textual (resumir, traduzir, gerar código) e roteia para o provedor LLM configurado (OpenAI, Gemini, Anthropic ou mock offline).

## Stack
| Camada | Tecnologia |
|--------|------------|
| CLI | `typer` |
| LLM | `openai` / `google-generativeai` / `anthropic` (auto-detect) |
| Utils | `projects/_shared` |

## Como rodar

```bash
pip install -r requirements.txt
python main.py resumir "texto longo aqui ..."
python main.py traduzir "Hello world" --idioma "português"
python main.py codigo "função fibonacci em python recursiva"
```

Sem API key, cai automaticamente no `MockLLMClient` (resposta determinística para smoke test).

## Output de exemplo

Sem nenhuma API key, o cliente cai no `MockLLMClient` (saída determinística — útil pra smoke test):

```bash
$ python main.py resumir "A IA está transformando setores inteiros..."
[provider=mock]
[mock-llm:e14c9a97] Resposta simulada para prompt de 140 chars. Configure OPENAI_API_KEY ou GEMINI_API_KEY para usar um provedor real.

$ python main.py traduzir "Hello world, how are you?" --idioma "português"
[provider=mock]
[mock-llm:5cdfea35] Resposta simulada para prompt de 25 chars. ...

$ python main.py codigo "função fibonacci recursiva" --linguagem python
[provider=mock]
[mock-llm:09a19368] Resposta simulada para prompt de 26 chars. ...
```

Com `OPENAI_API_KEY` exportada, a saída passa a vir do GPT-4o-mini (o cabeçalho muda para `[provider=openai]`).

## Entregáveis para portfólio
- CLI funcional com 3 comandos
- Auto-detecção de provedor (resiliente a falta de chaves)
- Padrão de wrapping multi-provider que se repete nos demais projetos

## Próximos passos
- Adicionar comando `chat` interativo
- Salvar histórico em SQLite
- Modo streaming (`--stream`)
