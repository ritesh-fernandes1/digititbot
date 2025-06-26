import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Topics DigitITBot should handle
ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile Models", "Waterfall Models", "Software Programming", "Coding",
    "Micro Processors", "Servers", "On-Premise Infrastructure", "Hybrid Infrastructure",
    "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM", "ServiceNow",
    "DevOps", "Problem Management", "Change Management", "Networking"
]

# Check if topic is relevant
def is_relevant_topic(user_input: str) -> bool:
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

# Main response logic
def get_bot_response(user_input: str) -> str:
    try:
        user_input = user_input.strip()
        if not user_input:
            return "⚠️ Please enter a valid question related to IT, cloud, or infrastructure."

        # Prepare messages based on topic
        if is_relevant_topic(user_input):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, a knowledgeable IT assistant. Answer user questions clearly and concisely.\n"
                        "✅ Use bullet points where helpful.\n"
                        "🔗 Always include **clickable markdown hyperlinks** to trusted IT sources like Microsoft, Cisco, AWS, etc."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, a helpful IT expert bot.\n"
                        "If the user's question is unrelated to IT, reframe it with an IT interpretation and respond.\n"
                        "✅ Use bullet points.\n"
                        "🔗 Always include clickable markdown-style hyperlinks when helpful."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}'. It's likely not IT-related directly, "
                        "so reinterpret the question in the context of information technology and answer accordingly."
                    )
                }
            ]

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "⚠️ Error: Something went wrong while processing your request.\n\n"
            f"```\n{str(e)}\n```\n\n"
            "[Check your API key and try again.](https://platform.openai.com/account/api-keys)"
        )