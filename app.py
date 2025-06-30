from flask import Flask, render_template, request, jsonify, session
from digititbot import get_bot_response
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save-name", methods=["POST"])
def save_name():
    data = request.get_json()
    full_name = data.get("full_name", "User")
    session["user_name"] = full_name
    return jsonify({"message": "Name saved!"})

@app.route("/chat", methods=["POST"])
def chat():
    if request.is_json:
        data = request.get_json()
        user_input = data.get("message", "")
        user_name = session.get("user_name", "You")
        bot_response = get_bot_response(user_input, user_name)
        return jsonify({"response": bot_response})
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

if __name__ == "__main__":
    app.run(debug=True, port=5050)