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
                        "Your name is DigitITBot. "
                        "You are an expert IT assistant that answers questions clearly and professionally. "
                        "Always use bullet points when listing items. Include relevant clickable hyperlinks. "
                        "⚠️ Never refer to yourself as DigiITBot or any other name."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Your name is DigitITBot. "
                        "You are a helpful IT assistant. When a question is unrelated to IT, "
                        "reinterpret it in an IT context and respond helpfully. "
                        "Always use bullet points and provide clickable hyperlinks. "
                        "⚠️ Never say your name is DigiITBot."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}'. "
                        "This might not be IT-specific, so reinterpret it in an IT context."
                    )
                }
            ]

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.6
        )

        raw_text = response.choices[0].message.content.strip()

        # ✅ Force-correct any hallucinated bot name
        clean_text = raw_text.replace("DigiITBot:", "DigitITBot:")
        return clean_text

    except Exception as e:
        return (
            "⚠️ Error: Something went wrong while processing your request.\n\n"
            f"```{str(e)}```\n\n"
            "Please try again or check your API key/config."
        )
