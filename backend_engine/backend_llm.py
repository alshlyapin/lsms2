from flask import Flask, jsonify, request
from transformers import AutoModelForCausalLM, AutoTokenizer


class GenerationConfig:
    def __init__(self, max_new_tokens=50, pad_token_id=2, eos_token_id=None):
        self.max_new_tokens = max_new_tokens
        self.pad_token_id = pad_token_id
        self.eos_token_id = eos_token_id

    def get_config(self):
        return {
            "max_new_tokens": self.max_new_tokens,
            "pad_token_id": self.pad_token_id,
            "eos_token_id": self.eos_token_id,
        }


app = Flask(__name__)

with app.app_context():
    base_model_id = "distilbert/distilgpt2"
    model = AutoModelForCausalLM.from_pretrained("./", device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_id,
        model_max_length=512,
        padding_side="left",
        add_eos_token=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    gen_config = GenerationConfig(eos_token_id=tokenizer.eos_token_id)
    print("--------Model and configuration are ready!--------------")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        question = data["text"]
        print(question)

        model_inputs = tokenizer(question, return_tensors="pt").to("cpu")
        generation_params = gen_config.get_config()
        answer = model.generate(**model_inputs, **generation_params)
        print(answer)
        return jsonify(
            {
                "predictions": tokenizer.decode(
                    answer[0], skip_special_tokens=True
                ).strip()
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# python backend_llm.py
# CMD: curl -X POST http://localhost:5000/predict -d "{\"text\":\"HSE is\"}"