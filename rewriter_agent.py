import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import time

app = Flask(__name__)
CORS(app)

# Configure Gemini API key (expecting it as environment variable)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

@app.route("/rewrite", methods=["POST"])
def rewrite_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided in the request body."}), 400

    original_text = data["text"]
    prompt = f"Rewrite the following passage to a 6th-grade reading level:\n\n{original_text}"

    try:
        for i in range(5):
            try:
                response = model.generate_content(prompt)
                rewritten_text = response.text
                return jsonify({"rewritten_text": rewritten_text}), 200
            except Exception as e:
                time.sleep(2 ** i)
        raise Exception("Max retries exceeded")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template("rewriter_agent.html")

if __name__ == "__main__":
   port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)