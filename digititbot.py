import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Topics allowed for digititbot to respond to
ALLOWED_TOPICS = [
    "Information Technology", "Mobile Devices", "PDAs", "Tablets", "Computers", "Computer Networking",
    "Laptop Computers", "Desktop Computers", "Agile Models", "Waterfall Models", "Software Programming",
    "Coding", "Micro Processors", "Servers", "On-Premise Infrastructure", "Hybrid Infrastructure",
    "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM", "ServiceNow"
]

def is_allowed_topic(message):
    return any(topic.lower() in message.lower() for topic in ALLOWED_TOPICS)

def get_bot_response(user_message):
    if not is_allowed_topic(user_message):
        return ("Sorry, I can only answer questions related to IT, Infrastructure, Cloud, Networking, "
                "ITSM, ITIL, ServiceNow, Programming, and Devices. Please ask a relevant question.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    "You are DigiITBot, an expert in Information Technology, Cloud Infrastructure, "
                    "Networking, Programming, ITSM, ServiceNow, and the ITIL framework. "
                    "You must include hyperlinks to reputable sources (e.g., Microsoft, AWS, ITIL, ServiceNow docs).")},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"