import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_bot_response(user_input):
    try:
        system_message = (
            "You are DigitITBot, an expert assistant for answering questions about Information Technology (IT), "
            "Cloud Technology, ITIL, ITSM, ServiceNow, IT Infrastructure (on-premise, hybrid, and cloud), Virtualization, "
            "Networking, Laptops, Desktops, Servers, Programming, and Software Engineering. "
            "If a user asks a question outside this scope, relate the topic to IT as best as possible and provide the answer "
            "with an IT context. Also provide helpful hyperlinks to trusted sources like Wikipedia, Microsoft, AWS, etc., when applicable. "
            "Use bullet points where appropriate and ensure all links are clickable."
        )

        completion = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"