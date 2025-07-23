import os
from flask import Flask, render_template, request, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import json
import time
import awsgi

# ✅ Load .env ONLY when running locally, not on Render
if os.environ.get("RENDER") != "true":
    load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # ✅ Allow CORS for frontend fetch

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    return Response(generate_streamed_response(request), mimetype='text/event-stream')

# ✅ Simple healthcheck route for deployment debugging
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return "✅ DigitITBot backend is healthy!", 200

def generate_streamed_response(req):
    try:
        data = req.get_json()
        user_msg = data.get("message", "")
        user_name = data.get("name", "User")
        language = data.get("language", "All")

        system_prompt = (
            "You are DigitITBot, an expert IT assistant. You provide concise, practical answers "
            "related to IT, cloud infrastructure, networking, ServiceNow, virtualization, coding, "
            "ITIL, ITSM, DevOps, and hybrid environments. Include useful bullet points and trusted hyperlinks in your answers. "
            "If the question is ambiguous, interpret it in an IT context."
        )

        chat_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_msg} (Programming Language: {language})"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=chat_messages,
            stream=True,
            temperature=0.7,
        )

        for chunk in response:
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0]["delta"]
                if "content" in delta:
                    yield f"data: {delta['content']}\n\n"

    except Exception as e:
        yield f"data: ⚠️ Error: {str(e)}\n\n"

# For AWS Lambda or Render
def lambda_handler(event, context):
    return awsgi.response(app, event, context)

# For local development
if __name__ == "__main__":
    app.run(debug=True, port=5050)
