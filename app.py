from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from digititbot import get_bot_response_stream
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "defaultsecret")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    user_name = data.get("userName")
    language = data.get("language")
    level = data.get("level")
    topic = data.get("topic")

    def generate():
        try:
            for token in get_bot_response_stream(user_input, user_name, language, level, topic):
                yield token
        except Exception as e:
            yield f"\n⚠️ Error: {str(e)}"

    return Response(stream_with_context(generate()), mimetype="text/plain")