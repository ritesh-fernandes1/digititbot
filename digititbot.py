import os
import openai
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

ALLOWED_TOPICS = [
    "IT", "Information Technology", "Mobile Devices", "PDAs", "Tablets",
    "Computers", "Computer Networking", "Laptop Computers", "Desktop Computers",
    "Agile Models", "Waterfall Models", "Software Programming", "Coding",
    "Micro Processors", "Servers", "On-Premise Infrastructure", "Hybrid Infrastructure",
    "Cloud Infrastructure Technology", "Virtualization", "ITIL", "ITSM", "ServiceNow"
]

def is_relevant_topic(user_input: str) -> bool:
    return any(topic.lower() in user_input.lower() for topic in ALLOWED_TOPICS)

def search_youtube_tutorials(query, language=None, level=None, max_results=5):
    api_key = os.getenv("YOUTUBE_API_KEY")
    base_url = "https://www.googleapis.com/youtube/v3/search"

    if language:
        query += f" tutorial in {language}"
    if level:
        query += f" for {level} learners"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])

        videos = []
        for item in items:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(f"- [{title}]({url})")
        return "\n".join(videos) if videos else "No tutorials found."

    except requests.exceptions.RequestException as e:
        return f"⚠️ YouTube API error: {str(e)}"

def get_bot_response(user_input: str) -> str:
    try:
        if is_relevant_topic(user_input):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are DigitITBot, an expert IT assistant. "
                        "Answer IT-related questions clearly, using bullet points where helpful, "
                        "and include relevant clickable hyperlinks. If the user requests video tutorials, "
                        "search YouTube using the topic, and apply filters if language or level is specified."
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
                        "Reinterpret non-IT questions in an IT context. "
                        "Provide concise answers with bullet points and clickable links. "
                        "If the user asks for tutorials, include YouTube results filtered by language or level if mentioned."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"The user asked: '{user_input}'. "
                        "It's not directly IT-related, so please relate it to IT and respond helpfully."
                    )
                }
            ]

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            "⚠️ Error: Something went wrong while processing your request.\n\n"
            f"```{str(e)}```\n\n"
            "Please try again or check your API key/config."
        )