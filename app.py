import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai

# ✅ Load .env ONLY locally (not on Render)
if os.environ.get("RENDER") != "true":
    load_dotenv()

# ✅ Initialize OpenAI client for v1.0+
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for frontend access

# ✅ Route: Home page
@app.route("/")
def index():
    return render_template("index.html")

# ✅ Route: POST /chat - handle incoming question
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
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

        # ✅ New OpenAI SDK v1.0+ call
        response = client.chat.completions.create(
            model="gpt-4",
            messages=chat_messages,
            temperature=0.7,
        )

        bot_reply = response.choices[0].message.content
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"}), 500

# ✅ Route: Healthcheck for Render diagnostics
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return "✅ DigitITBot backend is healthy!", 200

# ✅ Route: Google Search Console Verification
@app.route("/googlee310f7381f724126.html")
def google_verification():
    return app.send_static_file("googlee310f7381f724126.html")

# ✅ Local development only
if __name__ == "__main__":
    app.run(debug=True, port=5050)
