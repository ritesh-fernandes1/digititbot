from flask import Flask, render_template, request, jsonify
from digititbot import get_bot_response
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_input = data.get("message", "").strip()
    user_name = data.get("user_name", "User").strip()
    language = data.get("language", "").strip()
    level = data.get("level", "").strip()
    programming_language = data.get("programming_language", "").strip()

    # Defensive check: respond gracefully if no input
    if not user_input:
        return jsonify({"response": "⚠️ Please enter a valid question."})

    bot_response = get_bot_response(
        user_input,
        user_name=user_name,
        language=language,
        level=level,
        programming_language=programming_language
    )

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=5050)