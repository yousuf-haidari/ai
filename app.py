from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                reply = response.choices[0].message.content.strip()
            except Exception as e:
                reply = f"Error contacting AI service: {e}"

    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
