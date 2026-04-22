# -*- coding: utf-8 -*-
import os
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from peft import get_peft_config, get_peft_model, LoraConfig, TaskType

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
DATASET_PATH = "data/qa_climate_ml"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# Load QA pairs
ds = load_dataset("json", data_files={"train": f"{DATASET_PATH}/train.jsonl"}, split="train")

def format_example(example):
    prompt = f"User: {example['question']}\nAssistant:"
    # Tokenize with teacher‑forcing labels (the answer)
    tokens = tokenizer(prompt, return_tensors="pt")
    answer = tokenizer(example["answer"], return_tensors="pt")
    
    input_ids = tokens.input_ids[0]
    labels_ids = answer.input_ids[0]

    # Concatenate prompt+answer
    full_input_ids = torch.cat([input_ids, labels_ids])
    # Mask prompt part in labels
    full_labels = torch.cat([torch.full_like(input_ids, -100), labels_ids])
    
    return {
        "input_ids": full_input_ids, 
        "labels": full_labels, 
        "attention_mask": torch.ones_like(full_input_ids)
    }

ds = ds.map(format_example, remove_columns=ds.column_names)

# LoRA config – tiny rank, minimal GPU RAM
lora_cfg = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],   # Mistral architecture
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

base_model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    trust_remote_code=True,
    torch_dtype=torch.float16,
    device_map="auto"
)
model = get_peft_model(base_model, lora_cfg)

training_args = TrainingArguments(
    output_dir="finetuned/klima_ml",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=1,
    save_steps=100,
    evaluation_strategy="no",
    remove_unused_columns=False
)

trainer = Trainer(
    model=model, 
    args=training_args, 
    train_dataset=ds
)
trainer.train()

# Save LoRA adapters only (tiny)
model.save_pretrained("finetuned/klima_ml")
tokenizer.save_pretrained("finetuned/klima_ml")
print("Fine-tuning complete. Adapters saved to finetuned/klima_ml")
