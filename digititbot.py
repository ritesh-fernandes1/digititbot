import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Keywords for relevance check
ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile", "Waterfall", "Software", "Programming", "Coding",
    "Microprocessors", "Servers", "On-Premise", "Hybrid", "Cloud",
    "Virtualization", "ITIL", "ITSM", "ServiceNow", "Infrastructure"
]

def is_relevant_topic(user_input: str) -> bool:
    return any(keyword.lower() in user_input.lower() for keyword in ALLOWED_TOPICS)

def get_bot_response(user_input: str) -> str:
    try:
        messages = []

        if is_relevant_topic(user_input):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, an expert IT assistant. "
                        "Respond with accurate, helpful, and professional answers. "
                        "Use bullet points where helpful, and include clickable hyperlinks in markdown format."
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
                        "If a user asks a question that’s not obviously IT-related, reinterpret it in an IT context. "
                        "Always use:\n"
                        "- Bullet points\n"
                        "- Markdown-style clickable links\n"
                        "- An IT-relevant answer"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}'. It's not directly IT-related, "
                        "but please reinterpret and answer it in an IT context."
                    )
                }
            ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ API Error:\n\n```{str(e)}```"