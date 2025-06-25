from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from mangum import Mangum

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_message():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
        )
        reply = response.choices[0].message["content"]
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Use Mangum instead of awsgi
lambda_handler = Mangum(app)