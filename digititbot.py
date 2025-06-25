import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_TOPICS = [
    "Information Technology", "Cloud Technology", "Virtualization", "ITIL", "ITSM",
    "ServiceNow", "IT infrastructure", "Networking", "Laptops", "Desktops",
    "Tablets", "Servers", "Software Development", "Programming", "On-Premise Infrastructure",
    "Hybrid Infrastructure", "Agile Models", "Waterfall Models"
]

def is_allowed_topic(message):
    return any(topic.lower() in message.lower() for topic in ALLOWED_TOPICS)

def get_bot_response(user_input):
    if not is_allowed_topic(user_input):
        return "❌ Sorry, DigitITBot only answers questions related to IT, ITIL, ITSM, ServiceNow, infrastructure, networking, programming, and related technologies."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "You are DigitITBot, an expert assistant in Information Technology, IT Infrastructure, ITIL, ITSM, "
                    "ServiceNow, Networking, Devices, Cloud, Programming, and DevOps. "
                    "Answer only questions from these domains. Provide helpful links to documentation when possible."
                )},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"