import os
import openai
import markdown
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
        # Choose appropriate prompt based on topic relevance
        if is_relevant_topic(user_input):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, an expert IT assistant. "
                        "Answer IT-related questions with clear bullet points and clickable hyperlinks using Markdown."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, a helpful IT assistant. "
                        "When a question is not directly IT-related, reinterpret it in the context of IT. "
                        "Answer clearly using bullet points and clickable hyperlinks in Markdown."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}'. "
                        "It's not directly IT-related. Reinterpret it through the lens of IT and respond with helpful, clear information."
                    )
                }
            ]

        # Create response using OpenAI v1.0+ interface
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.6
        )

        # Convert Markdown to HTML for rendering
        markdown_text = response.choices[0].message.content.strip()
        html_response = markdown.markdown(markdown_text, extensions=['extra', 'sane_lists'])
        return html_response

    except Exception as e:
        return (
            "<p><strong>⚠️ Error:</strong> Something went wrong while processing your request.</p>"
            f"<pre>{str(e)}</pre>"
            "<p>Please try again or check your API key/config.</p>"
        )