import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_bot_response(user_input):
    prompt = f"""
    You are DigitITBot, an expert IT assistant. You answer only IT-related questions (including but not limited to: Information Technology, ITIL, ITSM, ServiceNow, Programming, Networking, Devices, Hybrid/Cloud/On-Prem Infrastructure).

    If the user's question seems unrelated to IT, try to reinterpret it with an IT context and answer accordingly.

    User: {user_input}
    DigitITBot:
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an IT expert bot named DigitITBot."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"