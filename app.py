# app.py
from flask import Flask, render_template, request, jsonify
from digititbot import chat_with_gpt, generate_quiz_questions
import markdown

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    name = data.get("name", "User")
    language = data.get("language", "All")

    gpt_response_md = chat_with_gpt(message, user_name=name, language=language)
    gpt_response_html = markdown.markdown(gpt_response_md)
    return jsonify({"response": gpt_response_html})

@app.route("/quiz/start", methods=["POST"])
def quiz_start():
    data = request.json
    topic = data.get("topic", "ITIL")
    num_questions = int(data.get("num_questions", 5))

    quiz_questions = generate_quiz_questions(topic=topic, num_questions=num_questions)
    # Ensure each question includes options and the correct answer
    formatted_questions = []
    for q in quiz_questions:
        formatted_questions.append({
            "question": q.get("question"),
            "options": q.get("options", []),
            "answer": q.get("answer")
        })
    return jsonify({"questions": formatted_questions})

@app.route("/quiz/submit", methods=["POST"])
def quiz_submit():
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
            feedback.append({"question": q["question"], "correct": False, "correct_answer": correct})

    return jsonify({"score": score, "total": len(questions), "feedback": feedback})

if __name__ == "__main__":
    app.run(debug=True)
