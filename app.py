from flask import Flask, render_template, request
from huggingface_hub import InferenceApi
import os

app = Flask(__name__)

# Initialize Hugging Face Inference client using environment variable
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
if not HF_TOKEN:
    raise ValueError("HUGGINGFACE_API_KEY environment variable not set.")

# Replace "gpt2" with your model of choice
client = InferenceApi(repo_id="gpt2", token=HF_TOKEN)

# Load business info
try:
    with open("FAQ.txt", "r", encoding="utf-8") as f:
        business_info = f.read().strip()
except FileNotFoundError:
    business_info = "No business info available."

@app.route("/", methods=["GET", "POST"])
def chat():
    reply = ""
    if request.method == "POST":
        user_question = request.form.get("question", "").strip()
        if user_question:
            prompt = f"""
You are a professional customer service assistant.

ONLY answer using the business information below.
If the answer is not in the info, say:
"I'm sorry, please contact the store directly for that information."

Business Information:
{business_info}

Customer Question:
{user_question}
"""
            try:
                # Hugging Face API call
                response = client(inputs=prompt)
                
                # Different models return different structures
                # For text generation models:
                if isinstance(response, list):
                    # e.g., [{"generated_text": "..."}]
                    reply = response[0].get("generated_text", "").strip()
                elif isinstance(response, dict):
                    # Sometimes directly a dict with 'generated_text'
                    reply = response.get("generated_text", "").strip()
                else:
                    reply = str(response)

            except Exception as e:
                reply = f"Error contacting AI service: {e}"

    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    app.run(debug=True)
