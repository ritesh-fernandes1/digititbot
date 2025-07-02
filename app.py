import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from digititbot import get_bot_response
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message")
        user_name = data.get("name", "User")
        language = data.get("language", "All Languages")
        level = data.get("level", "All Levels")
        programming_language = data.get("programming_language", "None")

        print("✅ POST /chat received:")
        print(f"Message: {user_input}")
        print(f"Name: {user_name}, Language: {language}, Level: {level}, Code Lang: {programming_language}")

        session["user_name"] = user_name
        bot_response = get_bot_response(user_input, user_name, language, level, programming_language)

        return jsonify({"response": bot_response})
    except Exception as e:
        print(f"❌ Error in /chat: {str(e)}")
        return jsonify({"response": "⚠️ Error: Could not connect to DigitITBot."}), 500

if __name__ == "__main__":
    app.run(debug=False)