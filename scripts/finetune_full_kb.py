# -*- coding: utf-8 -*-
import os
import torch
import argparse
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from peft import get_peft_model, LoraConfig, TaskType

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, default=os.getenv("HF_MODEL_ID", "Qwen/Qwen2.5-7B-Instruct"))
parser.add_argument("--epochs", type=int, default=5)
args = parser.parse_args()

MODEL_NAME = args.model_name
DATASET_PATH = "data/qa_full/train.jsonl"
OUTPUT_DIR = "finetuned/full_kb"

print(f"Loading tokenizer and model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# Load dataset
ds = load_dataset("json", data_files={"train": DATASET_PATH}, split="train")

def format_example(example):
    prompt = f"### Question: {example['question']}\n### Answer: {example['answer']}"
    # Tokenize as a single block for causal LM
    inputs = tokenizer(prompt, truncation=True, max_length=512, padding="max_length", return_tensors="pt")
    input_ids = inputs.input_ids[0]
    attention_mask = inputs.attention_mask[0]
    
    # For causal LM, labels are usually just input_ids (shifted internally)
    # We don't mask the prompt here for a simple "memorization" fine-tune
    return {"input_ids": input_ids, "labels": input_ids, "attention_mask": attention_mask}

print("Tokenizing dataset...")
ds = ds.map(format_example, remove_columns=ds.column_names)

# LoRA Configuration
lora_cfg = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

print("Initializing base model with MPS/CPU...")
# Use float16 for speed and MPS if available
base_model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto", # Should pick up MPS automatically
    trust_remote_code=True
)

model = get_peft_model(base_model, lora_cfg)
model.print_trainable_parameters()

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=5,
    learning_rate=3e-4,
    fp16=False, # MPS doesn't support fp16 in some versions, bf16/fp32 is safer
    logging_steps=1,
    save_strategy="no",
    remove_unused_columns=False,
    use_mps_device=True # Explicitly use MPS on Mac
)

print("Starting training...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=ds
)

trainer.train()

print(f"Saving adapters to {OUTPUT_DIR}")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print("Fine-tuning successful!")
