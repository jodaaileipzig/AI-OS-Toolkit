#!/usr/bin/env python3
"""Parameter-efficient LoRA fine-tuning runner for JSONL text data."""

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--epochs", type=float, default=1.0)
    args = parser.parse_args()

    from datasets import load_dataset
    from peft import LoraConfig, TaskType, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer, DataCollatorForLanguageModeling, Trainer, TrainingArguments

    dataset = load_dataset("json", data_files=args.data, split="train")
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = get_peft_model(model, LoraConfig(task_type=TaskType.CAUSAL_LM, r=16, lora_alpha=32, lora_dropout=0.05, target_modules="all-linear"))

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=1024)

    tokenized = dataset.map(tokenize, batched=True, remove_columns=dataset.column_names)
    training_args = TrainingArguments(output_dir=args.output, num_train_epochs=args.epochs, per_device_train_batch_size=1, gradient_accumulation_steps=8, learning_rate=2e-4, logging_steps=10, save_strategy="epoch", report_to="none")
    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    Trainer(model=model, args=training_args, train_dataset=tokenized, data_collator=collator).train()
    model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)


if __name__ == "__main__":
    main()