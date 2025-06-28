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
                        "You are DigitITBot (not DigiITBot), an expert IT assistant. "
                        "Always refer to yourself as DigitITBot in all replies. "
                        "Answer IT-related questions clearly, using bullet points where helpful, "
                        "and include relevant clickable hyperlinks."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot (not DigiITBot), a helpful IT assistant. "
                        "Always use the name DigitITBot in your responses. "
                        "Reinterpret non-IT questions in an IT context. "
                        "Provide concise answers with bullet points and clickable links."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}'. "
                        "It's not directly IT-related, so please relate it to IT and respond helpfully."
                    )
                }
            ]

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "⚠️ Error: Something went wrong while processing your request.\n\n"
            f"```{str(e)}```\n\n"
            "Please try again or check your API key/config."
        )