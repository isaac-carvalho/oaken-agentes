# 18 — Fine-Tuning de LLM com LoRA

> **Carreira Alura:** Engenharia de Agentes — Nível 2 (*Fine Tuning*)

Fine-tuning de um LLM open-source (default: **TinyLlama-1.1B**, swap fácil para Mistral-7B) com **LoRA** e quantização 4-bit (`bitsandbytes`). Inclui dataset de exemplo no formato instrução-resposta e script de inferência com adapter carregado.

## Stack
| Camada | Tecnologia |
|--------|------------|
| Modelo base | HuggingFace `transformers` |
| LoRA | `peft` |
| Quantização | `bitsandbytes` (opcional, requer CUDA) |
| Dataset | `datasets` |

## Como rodar

⚠️ Requer GPU (>= 8GB VRAM com TinyLlama 4-bit). Sem GPU, o script avisa e sai.

```bash
pip install -r requirements.txt
python train.py --base TinyLlama/TinyLlama-1.1B-Chat-v1.0 --epochs 1
python infer.py "Explique LoRA em 2 frases."
```

## Output de exemplo

### Dry-run sem GPU (validado)
```bash
$ python train.py --epochs 1
⚠️  Sem GPU detectada — fine-tuning real exige CUDA. Saindo (modo dry-run).

$ cat out/DRY_RUN.txt
base=TinyLlama/TinyLlama-1.1B-Chat-v1.0 epochs=1
```

### Dataset e formato
```bash
$ python -c "import json, pathlib; from train import format_example; \
    recs = [json.loads(l) for l in pathlib.Path('data/instrucoes.jsonl').read_text().splitlines()]; \
    print(f'{len(recs)} exemplos'); print(format_example(recs[0]))"
5 exemplos
### Instrução:
O que é LoRA?

### Resposta:
LoRA (Low-Rank Adaptation) treina apenas pequenas matrizes de baixa rank...
```

### Em uso real (com GPU)
```bash
$ python train.py --base TinyLlama/TinyLlama-1.1B-Chat-v1.0 --epochs 3
# Carrega TinyLlama em 4-bit (bitsandbytes), aplica LoRA r=16 nos
# módulos q_proj/v_proj, treina 3 epochs no dataset de instruções,
# salva o adapter PEFT em out/adapter/

$ python infer.py "Quando usar fine-tuning vs RAG?"
### Resposta: Use RAG para conhecimento factual atualizável; use fine-tuning para...
```

## Entregáveis para portfólio
- Script de fine-tuning reproduzível
- Adapter LoRA exportado em `out/adapter/`
- Demonstra entendimento de PEFT, quantização e custos de fine-tuning
