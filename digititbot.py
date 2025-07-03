
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_streaming_response(message, name, language):
    prompt = f"{name} asked a question in {language}:\n{message}\nRespond as an IT expert with markdown formatting and provide trusted links."

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in response:
        if hasattr(chunk.choices[0].delta, "content"):
            yield chunk.choices[0].delta.content
