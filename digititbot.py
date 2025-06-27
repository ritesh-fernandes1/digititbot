import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Topics we support
ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile Models", "Waterfall Models", "Software Programming", "Coding",
    "Micro Processors", "Servers", "On-Premise Infrastructure", "Hybrid Infrastructure",
    "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM", "ServiceNow"
]

def is_relevant_topic(user_input: str) -> bool:
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

def get_bot_response(user_input: str) -> str:
    try:
        if is_relevant_topic(user_input):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, an expert in IT, Cloud, ITIL, and Infrastructure. "
                        "Always answer with:\n"
                        "- Clear bullet points (if useful)\n"
                        "- Clickable links to references (Markdown format)\n"
                        "- Strictly IT-related context"
                    )
                },
                {"role": "user", "content": user_input}
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, an expert IT assistant. "
                        "If the user input is not directly IT-related, interpret it as if it were an IT concept. "
                        "Respond with:\n"
                        "- Bullet points\n"
                        "- Markdown-style hyperlinks\n"
                        "- Strong IT context"
                    )
                },
                {
                    "role": "user",
                    "content": f"The user asked: '{user_input}'. Please reinterpret it in an IT context and reply accordingly."
                }
            ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "⚠️ Error contacting OpenAI API.\n\n"
            f"```\n{str(e)}\n```\n"
            "Please check your API key or try again later."
        )