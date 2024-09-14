from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import load_dataset

def main():
    # Load the tokenizer and model
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Load the dataset
    dataset = load_dataset('json', data_files={'train': 'data/train_split.json', 'validation': 'data/val_split.json'})

    # Tokenize the dataset
    def tokenize_function(examples):
        return tokenizer(examples['text'], truncation=True, padding='max_length', max_length=512)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir='./model/fine_tuned_gpt2',
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        save_steps=500,
        save_total_limit=2,
        evaluation_strategy="epoch",
        logging_dir='./logs',
        logging_steps=10,
        learning_rate=5e-5,
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['validation']
    )

    # Start training
    trainer.train()

    # Save the final model
    trainer.save_model('./model/fine_tuned_gpt2')

if __name__ == "__main__":
    main()
