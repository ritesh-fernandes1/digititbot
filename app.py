# app.py
from flask import Flask, render_template, request, jsonify
from digititbot import chat_with_gpt, generate_quiz_questions  # Fixed import

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    name = data.get("name", "User")
    language = data.get("language", "All")

    response = chat_with_gpt(message, user_name=name, language=language)
    return jsonify({"response": response})

@app.route("/quiz/start", methods=["POST"])
def quiz_start():
    """Start quiz session with GPT-generated questions"""
    data = request.json
    topic = data.get("topic", "ITIL")
    num_questions = int(data.get("num_questions", 5))

    quiz_questions = generate_quiz_questions(topic=topic, num_questions=num_questions)
    return jsonify({"questions": quiz_questions})

@app.route("/quiz/submit", methods=["POST"])
def quiz_submit():
    """Score the quiz"""
    data = request.json
    answers = data.get("answers", [])
    questions = data.get("questions", [])

    score = 0
    feedback = []

    for i, q in enumerate(questions):
        correct = q.get("answer")
        user_ans = answers[i] if i < len(answers) else None
        if user_ans == correct:
            score += 1
            feedback.append({"question": q["question"], "correct": True})
        else:
            feedback.append({
                "question": q["question"],
                "correct": False,
                "correct_answer": correct
            })

    return jsonify({"score": score, "total": len(questions), "feedback": feedback})

@app.route("/ping", methods=["GET"])
def ping():
    """Health check endpoint for Render or monitoring services"""
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
