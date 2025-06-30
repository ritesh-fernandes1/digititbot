from flask import Flask, render_template, request, jsonify, session
from digititbot import get_bot_response
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/set-name", methods=["POST"])
def set_name():
    if request.is_json:
        data = request.get_json()
        name = data.get("fullName", "").strip()
        if name:
            session["full_name"] = name
            return jsonify({"message": "Name saved successfully."})
        return jsonify({"error": "No name provided"}), 400
    return jsonify({"error": "Unsupported Media Type"}), 415

@app.route("/chat", methods=["POST"])
def chat():
    if request.is_json:
        data = request.get_json()
        user_input = data.get("message", "")
        full_name = session.get("full_name", "You")
        bot_response = get_bot_response(user_input)
        return jsonify({
            "response": bot_response,
            "name": full_name
        })
    return jsonify({"error": "Unsupported Media Type"}), 415

if __name__ == "__main__":
    app.run(debug=True, port=5050)