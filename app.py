from flask import Flask, render_template, request, jsonify
from digititbot import get_bot_response, search_youtube_tutorials  # ✅ Added YouTube search support
import markdown

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("message", "")
    language = data.get("language", "").strip() or None  # ✅ Optional filter
    level = data.get("level", "").strip() or None        # ✅ Optional filter

    if "tutorial" in user_input.lower():
        tutorial_links = search_youtube_tutorials(user_input, language=language, level=level)  # ✅ YouTube results
        return jsonify({"response": tutorial_links})
    else:
        bot_response = get_bot_response(user_input)
        return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=5050)