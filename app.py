from flask import Flask, render_template, request, Response, stream_with_context
from flask_cors import CORS
from digititbot import get_streaming_response

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    user_name = data.get("name", "")
    language = data.get("language", "")

    def generate():
        for chunk in get_streaming_response(user_input, user_name, language):
            yield f"data: {chunk}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=5050)