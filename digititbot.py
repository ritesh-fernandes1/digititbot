import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile Models", "Waterfall Models", "Software Programming", "Coding",
    "Micro Processors", "Servers", "On-Premise Infrastructure", "Hybrid Infrastructure",
    "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM", "ServiceNow",
    "DevOps", "Problem Management", "Incident Management", "Change Management", "Networking"
]

def is_relevant_topic(user_input: str) -> bool:
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

def get_bot_response(user_input: str) -> str:
    try:
        messages = []

        if is_relevant_topic(user_input):
            messages.append({
                "role": "system",
                "content": (
                    "You are DigitITBot, an expert IT assistant. "
                    "Respond to IT-related questions clearly, using:\n"
                    "- Bullet points where useful\n"
                    "- Clickable hyperlinks (Markdown format)\n"
                    "Focus on IT, infrastructure, networking, ITIL, and related domains."
                )
            })
            messages.append({"role": "user", "content": user_input})
        else:
            messages.append({
                "role": "system",
                "content": (
                    "You are DigitITBot, a helpful IT assistant. "
                    "If a question is not directly IT-related, reinterpret it in an IT context "
                    "and answer accordingly. Use:\n"
                    "- Bullet points\n"
                    "- Clickable Markdown links"
                )
            })
            messages.append({
                "role": "user",
                "content": (
                    f"The user asked: '{user_input}'. "
                    "Please respond in an IT context."
                )
            })

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "⚠️ Error: Something went wrong while processing your request.\n\n"
            f"```\n{str(e)}\n```\n\n"
            "Please try again or check your API key."
        )