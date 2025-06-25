import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_bot_response(user_input):
    if not openai.api_key:
        return "OpenAI API key not found."

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are DigiITBot, an expert IT assistant. "
                        "Answer ONLY questions about IT, ITIL, ITSM, ServiceNow, Cloud, Hybrid Infra, Programming, Networking, and Devices. "
                        "Always include a helpful reference URL."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
            temperature=0.5,
        )
        reply = completion.choices[0].message["content"]
        return reply

    except Exception as e:
        return f"Error: {str(e)}"