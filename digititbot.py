import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define topics the bot should handle
ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile Models", "Waterfall Models", "Software Programming", "Coding",
    "Micro Processors", "Servers", "On-Premise Infrastructure", "Hybrid Infrastructure",
    "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM", "ServiceNow"
]

# Helper function to check relevance
def is_relevant_topic(user_input: str) -> bool:
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

# Main response function
def get_bot_response(user_input: str) -> str:
    try:
        # If relevant question, ask OpenAI directly
        if is_relevant_topic(user_input):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, an expert IT assistant. "
                        "Answer IT-related questions with concise, clear information. "
                        "Always include bullet points where relevant and helpful hyperlinks."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        else:
            # Try to reinterpret unrelated queries in an IT context
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, a helpful IT assistant. "
                        "When a question is not directly IT-related, reinterpret it in the context of IT and provide an answer. "
                        "Always use bullet points when useful and add clickable hyperlinks to reliable sources."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}'. "
                        "It's not directly IT-related, but reinterpret it in an IT context and respond accordingly."
                    )
                }
            ]

        # Use new OpenAI v1.0+ API interface
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