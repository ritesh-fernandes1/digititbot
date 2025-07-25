import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile Models", "Waterfall Models", "Software Programming", "Coding",
    "Micro Processors", "Servers", "On-Premise Infrastructure", "Hybrid Infrastructure",
    "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM", "ServiceNow"
]

def is_relevant_topic(user_input: str) -> bool:
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

def get_streaming_response(user_input: str, user_name: str, language: str):
    try:
        if is_relevant_topic(user_input):
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"You are DigitITBot, a highly skilled IT assistant for {user_name}. "
                        "Answer all IT questions precisely. Use bullet points, embed relevant hyperlinks, "
                        f"and prioritize information relevant to '{language}' where appropriate."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"You are DigitITBot, a helpful IT assistant for {user_name}. "
                        "Reframe unrelated questions in an IT context. Use bullet points and links when helpful. "
                        f"Prioritize answers based on '{language}' if applicable."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}', which is not clearly IT-related. "
                        "Please interpret it in an IT context and respond accordingly."
                    )
                }
            ]

        # Stream GPT-4o response
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.6,
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                yield delta.content

    except Exception as e:
        yield f"⚠️ Error: {str(e)}"