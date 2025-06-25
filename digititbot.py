import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load your OpenAI API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_bot_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, an expert in Information Technology, Cloud Infrastructure, "
                        "Networking, Programming, ITSM, ServiceNow, and the ITIL framework. "
                        "You must include hyperlinks to reputable sources (e.g., Microsoft, AWS, ITIL, ServiceNow docs)."
                    )
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"