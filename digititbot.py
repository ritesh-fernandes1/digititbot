# digititbot.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(message, user_name="User", language="All"):
    """Regular chatbot responses."""
    prompt = f"""
    You are DigitITBot, an IT tutor specializing in ITIL, ITSM, ServiceNow, Cloud, Networking & DevOps.
    Student name: {user_name}
    Preferred programming language: {language}
    Question: {message}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful IT tutor bot."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def generate_quiz_questions(topic="ITIL", num_questions=5):
    """
    Generate quiz questions dynamically with GPT.
    Output format: JSON list of dicts with 'question', 'options', 'answer'.
    """
    prompt = f"""
    Generate {num_questions} multiple-choice quiz questions on the topic: {topic}.
    Each question should be scenario-based and test ITIL/Cloud/ITSM/DevOps concepts.
    Format the output as strict JSON like this:
    [
      {{
        "question": "What does ITIL stand for?",
        "options": ["A. IT Infrastructure Library", "B. Internet Technology Integrated Language", "C. Information Technology and Innovation Lab", "D. Infrastructure Testing in Linux"],
        "answer": "A"
      }}
    ]
    Do NOT include explanations, only valid JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a quiz generator for IT students."},
                  {"role": "user", "content": prompt}],
        temperature=0.6
    )

    import json
    try:
        quiz_json = json.loads(response.choices[0].message.content.strip())
    except Exception:
        quiz_json = []

    return quiz_json
