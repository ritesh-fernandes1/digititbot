import os
import requests
import markdown
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BOT_NAME = os.getenv("BOT_NAME", "DigitITBot")

# In-memory history log (demo purpose only)
user_video_history = {}

def fetch_youtube_videos(query, language=None, level=None, max_results=3):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results,
        "safeSearch": "strict"
    }

    if language and language != "All Languages":
        params["relevanceLanguage"] = language

    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        return ["⚠️ Could not fetch video suggestions."]

    videos = response.json().get("items", [])
    results = []
    for video in videos:
        title = video["snippet"]["title"]
        video_id = video["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        if level and level != "All Levels":
            if level.lower() not in title.lower():
                continue
        results.append(f"[{title}]({video_url})")

    return results if results else ["❗ No suitable video tutorials found."]

def get_bot_response(user_input, user_name="User", language=None, level=None, programming_language=None):
    name_tag = f"{user_name.strip()}" if user_name else "User"

    system_prompt = (
        f"You are {BOT_NAME}, a helpful IT assistant. "
        f"You specialize in IT, Cloud, ITIL, ServiceNow, DevOps, Networking, Hybrid Infrastructure, Devices, "
        f"and Programming. Provide URLs when helpful. If the question relates to coding, explain clearly with examples."
    )

    if programming_language and programming_language != "None":
        user_input = f"{user_input} (Please answer using {programming_language})"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.6
        )
        bot_reply = response.choices[0].message.content.strip()

        if "tutorial" in user_input.lower() or "video" in user_input.lower():
            yt_videos = fetch_youtube_videos(user_input, language, level)
            user_video_history.setdefault(name_tag, []).extend(yt_videos)
            bot_reply += "\n\n📺 **YouTube Tutorials to get started:**\n" + "\n".join(yt_videos)

        return markdown.markdown(bot_reply)

    except Exception as e:
        print(f"❌ Error in get_bot_response: {str(e)}")
        return "⚠️ Error: Could not connect to DigitITBot."