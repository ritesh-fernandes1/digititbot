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
    "DevOps", "Problem Management", "Change Management", "Networking"
]

def is_relevant_topic(user_input: str) -> bool:
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

def get_bot_response(user_input: str) -> str:
    try:
        user_input = user_input.strip()
        if not user_input:
            return "⚠️ Please enter a valid question related to IT, cloud, or infrastructure."

        messages = []

        if is_relevant_topic(user_input):
            messages.append({
                "role": "system",
                "content": (
                    "You are DigitITBot, a helpful expert on IT, Cloud, Infrastructure, Networking, "
                    "ITSM, and ServiceNow. You respond clearly and include:\n"
                    "- Bullet points for structured answers\n"
                    "- Clickable hyperlinks in markdown"
                )
            })
            messages.append({"role": "user", "content": user_input})
        else:
            messages.append({
                "role": "system",
                "content": (
                    "You are DigitITBot, an IT assistant. The user's query may not be directly IT-related. "
                    "Reinterpret it from an IT or computing perspective and answer accordingly. Always include:\n"
                    "- Bullet points when helpful\n"
                    "- Clickable hyperlinks in markdown"
                )
            })
            messages.append({
                "role": "user",
                "content": f"The user asked: '{user_input}'. Reframe and explain it in an IT context."
            })

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "⚠️ Error while processing your request.\n\n"
            f"```\n{str(e)}\n```\n\n"
            "[Check your API key and try again](https://platform.openai.com/account/api-keys)."
        )