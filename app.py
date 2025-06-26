from flask import Flask, render_template, request, jsonify
from digititbot import get_bot_response  # ✅ Ensure file is named digititbot.py
import markdown

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Try to parse incoming JSON (even if headers are missing)
        data = request.get_json(force=True)
        user_input = data.get("message", "").strip()

        # Handle empty messages
        if not user_input:
            return jsonify({
                "response": "⚠️ Please enter a valid question related to IT, cloud, or infrastructure."
            })

        # Get the bot response
        bot_response = get_bot_response(user_input)
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({
            "response": f"⚠️ Error processing your input. Please try again later.\n\n```{str(e)}```"
        })

if __name__ == "__main__":
    app.run(debug=True)