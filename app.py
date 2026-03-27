import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Summarizer agent is running",
        "usage": "POST /summarize with JSON: {\"text\": \"your long text\"}"
    })

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Please provide 'text' in request body"}), 400

    prompt = f"Summarize the following text in 3 short bullet points:\n\n{text}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({
        "input": text,
        "summary": response.text
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
