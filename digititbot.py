import openai
import os

def ask_openai(message):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        return "OpenAI API key not set."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are DigiITBot, a helpful expert in IT, cloud, networking, ServiceNow, and programming. Always include a hyperlink to an official resource."},
                {"role": "user", "content": message}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"