import os
import openai
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BOT_NAME = os.getenv("BOT_NAME", "DigitITBot")

ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile Models", "Waterfall Models", "Software Programming", "Coding",
    "Micro Processors", "Servers", "On-Premise Infrastructure", "Hybrid Infrastructure",
    "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM", "ServiceNow"
]

def is_relevant_topic(user_input: str) -> bool:
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

def search_youtube(query: str, language="", level=""):
    try:
        base_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": f"{query} tutorial {language} {level}".strip(),
            "key": YOUTUBE_API_KEY,
            "type": "video",
            "maxResults": 3
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        videos = []
        for item in data.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(f"[{title}]({url})")

        if videos:
            return "\n\n**📺 Recommended Video Tutorials:**\n" + "\n".join(videos)
        else:
            return "\n\n❗No videos found matching your criteria."

    except Exception as e:
        return f"\n\n⚠️ Could not fetch YouTube videos: `{str(e)}`"

def get_bot_response(user_input, user_name="User", language="", level="", programming_language=""):
    try:
        query_context = ""
        if language:
            query_context += f"\nPreferred Language: {language}."
        if level:
            query_context += f"\nTutorial Level: {level}."
        if programming_language:
            query_context += f"\nProgramming Language: {programming_language}."

        if is_relevant_topic(user_input) or programming_language:
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"You are {BOT_NAME}, a professional IT assistant. "
                        "Answer all questions in natural tone with helpful detail. "
                        "Use bullet points where needed. Add hyperlinks where applicable. "
                        "Respect language preference and tutorial level. "
                        "If programming is involved, tailor the explanation accordingly."
                    )
                },
                {
                    "role": "user",
                    "content": f"{user_name} asked: {user_input}{query_context}"
                }
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"You are {BOT_NAME}, a professional IT assistant. "
                        "The user has asked something that may not be directly IT-related. "
                        "Please interpret it within the context of IT and respond with helpful insight."
                    )
                },
                {
                    "role": "user",
                    "content": f"{user_name} asked: {user_input}{query_context}"
                }
            ]

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.6
        )

        bot_reply = response.choices[0].message.content.strip()

        # Check if it's a tutorial request
        if "tutorial" in user_input.lower() or "video" in user_input.lower() or "learn" in user_input.lower():
            youtube_suggestions = search_youtube(user_input, language, level)
            bot_reply += youtube_suggestions

        return bot_reply

    except Exception as e:
        return (
            f"⚠️ Error: Something went wrong while processing your request.\n\n"
            f"```{str(e)}```\n\n"
            "Please try again or check your API keys."
        )