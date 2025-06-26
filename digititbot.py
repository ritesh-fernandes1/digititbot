import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Topics considered relevant to IT
ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile", "Waterfall", "Software", "Programming", "Coding",
    "Microprocessors", "Servers", "Infrastructure", "On-Premise", "Hybrid",
    "Cloud", "Virtualization", "ITIL", "ITSM", "ServiceNow", "DevOps", "Network"
]

def is_relevant_topic(user_input: str) -> bool:
    """Check if user input contains IT-related keywords."""
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

def get_bot_response(user_input: str) -> str:
    """Generate response using OpenAI, including bullet points and links."""
    try:
        client = openai.OpenAI()

        # Decide prompt based on relevance
        if is_relevant_topic(user_input):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, a helpful and professional IT assistant. "
                        "Answer user queries with accurate, clear responses. "
                        "Always use bullet points when helpful and include clickable hyperlinks to official sources or documentation."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, a professional IT assistant. "
                        "If a user's question is not about IT directly, reinterpret it from an IT/infrastructure/software/networking perspective. "
                        "Always answer with bullet points where helpful and include clickable hyperlinks."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}'. "
                        "Please reinterpret this in the context of IT and answer accordingly."
                    )
                }
            ]

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "⚠️ Error while processing your request:\n\n"
            f"```{str(e)}```\n\nPlease check your API key or try again later."
        )