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

## Entregáveis para portfólio
- Script de fine-tuning reproduzível
- Adapter LoRA exportado em `out/adapter/`
- Demonstra entendimento de PEFT, quantização e custos de fine-tuning
