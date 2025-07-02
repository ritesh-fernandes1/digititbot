import os
import openai
from dotenv import load_dotenv
from markdown import markdown

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BOT_NAME = os.getenv("BOT_NAME", "DigitITBot")

def get_bot_response(user_input, user_name=None, language=None, level=None, topic=None):
    messages = [
        {
            "role": "system",
            "content": (
                f"You are {BOT_NAME}, an expert IT assistant. "
                f"Respond to IT-related questions clearly with helpful links. "
                f"If the user gives filters like language or level, use them for tutorial recommendations."
            )
        },
        {
            "role": "user",
            "content": f"{user_name or 'User'} asked: {user_input}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content

def get_bot_response_stream(user_input, user_name=None, language=None, level=None, topic=None):
    messages = [
        {
            "role": "system",
            "content": (
                f"You are {BOT_NAME}, an expert IT assistant. "
                f"Respond to IT-related questions clearly with helpful links. "
                f"If the user gives filters like language or level, use them for tutorial recommendations."
            )
        },
        {
            "role": "user",
            "content": f"{user_name or 'User'} asked: {user_input}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.6,
        stream=True  # Enable streaming
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content