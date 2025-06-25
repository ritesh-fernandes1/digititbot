from flask import Flask, request, render_template, jsonify
from digititbot import get_bot_response  # ✅ Corrected module name
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "Please enter a valid question."}), 400
    try:
        bot_response = get_bot_response(user_input)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)