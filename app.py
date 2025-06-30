import os
from flask import Flask, render_template, request, jsonify, session
from digititbot import get_bot_response
from dotenv import load_dotenv
import markdown

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or "fallbacksecret"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/setname", methods=["POST"])
def set_name():
    data = request.get_json()
    session["full_name"] = data.get("full_name", "")
    return jsonify({"status": "ok"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("message", "")
    full_name = session.get("full_name", "")
    bot_response = get_bot_response(user_input, full_name=full_name)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=5050)