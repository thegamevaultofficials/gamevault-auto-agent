import os, random, requests
from gtts import gTTS
from moviepy.editor import *

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_script():
    topics = ["Top 5 hidden features in GTA 5", "The dark story of Minecraft's Herobrine", "Why Free Fire was banned", "5 secret places in BGMI", "The man who played GTA 5 for 10 years"]
    chosen_topic = random.choice(topics)
    print(f"Chosen Topic: {chosen_topic}")
    return chosen_topic, f"This is the untold documentary of {chosen_topic}. Number one will blow your mind."

topic, script_text = generate_script()

with open("title.txt","w") as f:
    f.write(topic)

print("Creating voice...")
tts = gTTS(text=script_text, lang='en', slow=False)
tts.save("voice.mp3")
audio = AudioFileClip("voice.mp3")
print(f"Voice duration: {audio.duration}")

video_clips = []
headers = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else {}

try:
    search_query = random.choice(["gaming setup rgb", "esports gaming", "video game controller", "gaming pc neon", "cyberpunk city"])
    print(f"Searching Pexels for: {search_query}")
    url = f"https://api.pexels.com/videos/search?query={search_query}&per_page=10&orientation=landscape"
    r = requests.get(url, headers=headers, timeout=20)
    print(f"Pexels status: {r.status_code}")
    for v in r.json().get("videos", [])[:6]:
        best = sorted(v['video_files'], key=lambda x: x['width'], reverse=True)[0]
        tmp = f"temp_{len(video_clips)}.mp4"
        with open(tmp, 'wb') as f:
            f.write(requests.get(best['link'], timeout=20).content)
        clip = VideoFileClip(tmp).resize(height=720).crop(width=1280, height=720, x_center=640, y_center=360)
        video_clips.append(clip)
except Exception as e:
    print(f"Pexels error: {e}")

if len(video_clips) == 0:
    print("Using backup colors")
    for i in range(8):
        color = (random.randint(10,255), random.randint(10,255), random.randint(10,255))
        clip = ColorClip((1280,720), color=color, duration=3)
        video_clips.append(clip)

final_clips = []
time_cursor = 0
while time_cursor < audio.duration:
    c = random.choice(video_clips)
    if c.duration > 3:
        c = c.subclip(random.uniform(0, c.duration-3), random.uniform(0, c.duration-3)+3)
    final_clips.append(c.set_start(time_cursor))
    time_cursor += c.duration

video = CompositeVideoClip(final_clips, size=(1280,720)).set_duration(audio.duration)
video = video.set_audio(audio)
video.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("DONE!")
