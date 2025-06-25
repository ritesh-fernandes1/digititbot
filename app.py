from flask import Flask, request, jsonify, render_template
from digiitbot import get_bot_response
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# ✅ Homepage route
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')  # This should load the UI

# ✅ POST endpoint for chatbot
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    try:
        response = get_bot_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500