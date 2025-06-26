from flask import Flask, render_template, request, jsonify
from DigitITBot import get_bot_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if request.is_json:
        user_input = request.json.get("message", "")
        bot_response = get_bot_response(user_input)
        return jsonify({"response": bot_response})
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415