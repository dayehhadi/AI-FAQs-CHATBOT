from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost"}})  # Adjust origin as needed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the fine-tuned model and tokenizer
model_path = './model/fine_tuned_gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Ensure model is in evaluation mode
model.eval()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '').strip()
    logger.info(f"User input: {user_input}")

    if not user_input:
        return jsonify({'response': 'Please enter a valid message.'})

    # Format the input
    prompt = f"Question: {user_input}\nAnswer:"
    inputs = tokenizer.encode(prompt, return_tensors='pt')

    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=512,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_p=0.95,
            top_k=60
        )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract the answer part
    if "Answer:" in answer:
        answer = answer.split('Answer:')[-1].strip()
    else:
        answer = "I'm sorry, I didn't understand that. Could you please rephrase?"

    logger.info(f"Bot response: {answer}")
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
