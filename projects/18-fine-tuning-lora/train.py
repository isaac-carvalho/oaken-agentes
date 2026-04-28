"""Fine-tuning LoRA com PEFT."""
from __future__ import annotations

from pathlib import Path

import torch
import typer

app = typer.Typer()
OUT = Path(__file__).parent / "out"
DATA = Path(__file__).parent / "data" / "instrucoes.jsonl"


def format_example(rec: dict) -> str:
    return f"### Instrução:\n{rec['instruction']}\n\n### Resposta:\n{rec['response']}"


@app.command()
def main(
    base: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    epochs: int = 1,
    lr: float = 2e-4,
    batch: int = 4,
) -> None:
    if not torch.cuda.is_available():
        typer.echo("⚠️  Sem GPU detectada — fine-tuning real exige CUDA. Saindo (modo dry-run).")
        OUT.mkdir(exist_ok=True)
        (OUT / "DRY_RUN.txt").write_text(f"base={base} epochs={epochs}\n")
        return

    from datasets import load_dataset
    from peft import LoraConfig, get_peft_model, TaskType
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        Trainer,
        TrainingArguments,
    )

    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
    tok = AutoTokenizer.from_pretrained(base)
    tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(base, quantization_config=bnb, device_map="auto")
    lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type=TaskType.CAUSAL_LM, target_modules=["q_proj", "v_proj"])
    model = get_peft_model(model, lora)

    ds = load_dataset("json", data_files=str(DATA), split="train")

    def tokenize(rec):
        text = format_example(rec) + tok.eos_token
        enc = tok(text, truncation=True, padding="max_length", max_length=256)
        enc["labels"] = enc["input_ids"].copy()
        return enc

    ds = ds.map(tokenize, remove_columns=ds.column_names)

    args = TrainingArguments(
        output_dir=str(OUT / "checkpoints"),
        per_device_train_batch_size=batch,
        num_train_epochs=epochs,
        learning_rate=lr,
        logging_steps=5,
        save_strategy="epoch",
        report_to=[],
    )
    Trainer(model=model, args=args, train_dataset=ds).train()
    model.save_pretrained(str(OUT / "adapter"))
    tok.save_pretrained(str(OUT / "adapter"))
    typer.echo(f"Adapter salvo em {OUT / 'adapter'}")


if __name__ == "__main__":
    app()
