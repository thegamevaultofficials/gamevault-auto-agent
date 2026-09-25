import os, random, requests, json
from gtts import gTTS
from moviepy.editor import *
import datetime

# --- KEYS FROM GITHUB SECRETS ---
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 1. AUTO TOPIC + AUTO SCRIPT (Brain of the Agent)
def generate_script():
    topics = [
        "Top 5 hidden features in GTA 5 that 99% missed",
        "The dark story of Minecraft's Herobrine explained",
        "Why Free Fire was banned and the real truth",
        "5 secret places in BGMI Erangel you never knew",
        "The man who played GTA 5 for 10 years straight",
        "How Rockstar hides real life mysteries in GTA",
        "The most expensive skins in gaming history"
    ]
    chosen_topic = random.choice(topics)
    print(f"Chosen Topic: {chosen_topic}")

    # If you have Groq key, it will write a fresh script, else use topic as script
    if GROQ_API_KEY:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            prompt = f"Write a 150 word viral YouTube Shorts documentary script for gaming topic: {chosen_topic}. Hook in first 3 seconds, 5 points, keep it exciting, no intro like 'welcome'. Just the script."
            data = {"model": "llama-3.3-70b-versatile", "messages": [{"role":"user","content":prompt}]}
            res = requests.post(url, headers=headers, json=data, timeout=30)
            script = res.json()['choices'][0]['message']['content']
            return chosen_topic, script
        except Exception as e:
            print(f"Groq failed, using fallback: {e}")
            return chosen_topic, f"Did you know {chosen_topic}? Here are the facts that will shock you. Let's dive into the gaming documentary."
    else:
        return chosen_topic, f"This is the untold documentary of {chosen_topic}. Number one will blow your mind. Let's start."

topic, script_text = generate_script()
print(f"FINAL SCRIPT: {script_text}")

# Save topic for YouTube title later
with open("title.txt","w") as f:
    f.write(topic)

# 2. VOICEOVER
print("Creating voice...")
tts = gTTS(text=script_text, lang='en', slow=False)
tts.save("voice.mp3")
audio = AudioFileClip("voice.mp3")
print(f"Voice duration: {audio.duration}")

# 3. GET GAMEPLAY FOOTAGE
video_clips = []
search_query = topic.split("in")[-1] if "in" in topic else "gta gameplay"
headers = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else {}

try:
    url = f"https://api.pexels.com/videos/search?query={search_query}&per_page=10&orientation=landscape"
    r = requests.get(url, headers=headers, timeout=20)
    for v in r.json().get("videos", [])[:6]:
        best = sorted(v['video_files'], key=lambda x: x['width'], reverse=True)[0]
        tmp = f"temp_{len(video_clips)}.mp4"
        with open(tmp, 'wb') as f:
            f.write(requests.get(best['link'], timeout=20).content)
        clip = VideoFileClip(tmp).resize(height=720).crop(width=1280, height=720, x_center=640, y_center=360)
        video_clips.append(clip)
except Exception as e:
    print(f"Pexels error: {e}")

# BACKUP - Never fail
if len(video_clips) == 0:
    print("Using backup colors")
    for i in range(8):
        color = (random.randint(10,255), random.randint(10,255), random.randint(10,255))
        clip = ColorClip((1280,720), color=color, duration=3)
        video_clips.append(clip)

# 4. AUTO EDITING
final_clips = []
time_cursor = 0
while time_cursor < audio.duration:
    c = random.choice(video_clips)
    if c.duration > 3:
        c = c.subclip(random.uniform(0, c.duration-3), random.uniform(0, c.duration-3)+3)
    final_clips.append(c.set_start(time_cursor))
    time_cursor += c.duration

# Add Title Text
txt = TextClip(topic, fontsize=60, color='white', font='Arial-Bold', stroke_color='black', stroke_width=3, method='caption', size=(1100, None))
txt = txt.set_pos('center').set_duration(min(4, audio.duration))

video = CompositeVideoClip(final_clips + [txt], size=(1280,720)).set_duration(audio.duration)
video = video.set_audio(audio)

# 5. EXPORT - Ready to upload
video.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("AGENT DONE - Video created: final_video.mp4")
