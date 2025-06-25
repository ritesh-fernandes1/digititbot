import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

ALLOWED_TOPICS = [
    "IT", "Mobile Devices", "PDAs", "Tablets", "Computers", "Computer Networking",
    "Laptop Computers", "Desktop Computers", "Agile Models", "Waterfall Models",
    "Software Programming", "Coding", "Micro Processors", "Servers", "On-Premise Infrastructure",
    "Hybrid Infrastructure", "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM",
    "ServiceNow", "General IT", "IT Infrastructure"
]

def get_bot_response(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are DigiITBot, an expert assistant that only answers questions related to "
                "Information Technology, Mobile Devices, Computers, Networking, Agile/Waterfall Models, "
                "Programming, Cloud/Hybrid Infrastructure, ITIL, ITSM, and ServiceNow. If the question is "
                "outside this scope, politely decline and say you only answer IT-related questions. "
                "For valid answers, provide trusted external URLs for further reading."
            )
        },
        {"role": "user", "content": user_query}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5,
        max_tokens=700
    )

    return response['choices'][0]['message']['content'].strip()