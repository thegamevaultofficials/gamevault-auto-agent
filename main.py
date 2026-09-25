import os, json, random, requests, textwrap
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
from voice import make_voiceover # your Edge-TTS hi-IN-MadhurNeural

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- 1. TOPIC TRACKING ---
def get_next_topic():
    with open("topics.txt","r", encoding="utf-8") as f:
        all_topics = [l.strip() for l in f if l.strip()]

    used = []
    if os.path.exists("used_topics.json"):
        with open("used_topics.json","r") as f:
            used = json.load(f)

    available = [t for t in all_topics if t not in used]
    if not available: # reset if all used
        available = all_topics
        used = []

    topic = random.choice(available)
    used.append(topic)
    with open("used_topics.json","w") as f:
        json.dump(used, f, indent=2)

    return topic

def generate_script(topic):
    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY is missing in GitHub Secrets! Run fails loudly as intended.")

    last_err = None
    for attempt in range(3):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            prompt = f"Write 150 word viral YouTube Shorts script for '{topic}' in Hinglish mix. Hook, 5 points, energetic."
            data = {"model": "openai/gpt-oss-20b", "messages": [{"role":"user","content":prompt}]}
            r = requests.post(url, headers=headers, json=data, timeout=30)
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception as e:
            last_err = e
            print(f"Groq attempt {attempt+1} failed: {e}")

    raise Exception(f"Groq failed 3 times: {last_err}")

def create_thumbnail(topic, out="thumbnail.png"):
    img = Image.new("RGB", (1280,720), (15,15,15))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
    except:
        font = ImageFont.load_default()
    text = textwrap.fill(topic, width=25)
    draw.text((50,200), text, font=font, fill="white")
    img.save(out)
    return out

# --- MAIN ---
topic = get_next_topic()
script = generate_script(topic)

with open("title.txt","w", encoding="utf-8") as f:
    f.write(topic)

print(f"Topic: {topic}")
# 2. VOICE - Edge-TTS
make_voiceover(script)
audio = AudioFileClip("voice.mp3")

# Pexels logic - SAME as your V2 (unchanged)
video_clips = []
headers = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else {}
try:
    q = random.choice(["gaming setup rgb", "esports gaming", "gaming pc neon"])
    url = f"https://api.pexels.com/videos/search?query={q}&per_page=15&orientation=landscape"
    r = requests.get(url, headers=headers, timeout=30)
    for v in r.json().get("videos", [])[:8]:
        best = sorted(v['video_files'], key=lambda x: x['width'], reverse=True)[0]
        tmp = f"temp_{len(video_clips)}.mp4"
        with open(tmp, 'wb') as f:
            f.write(requests.get(best['link'], timeout=20).content)
        base = VideoFileClip(tmp).resize(height=720).crop(width=1280, height=720, x_center=640, y_center=360)
        video_clips.append(base)
except Exception as e:
    print(e)

if not video_clips:
    video_clips = [ColorClip((1280,720), color=(20,20,20), duration=5)]

final_parts = []
cursor = 0
while cursor < audio.duration:
    c = random.choice(video_clips)
    dur = min(3, c.duration, audio.duration-cursor)
    part = c.subclip(0, dur).set_start(cursor)
    final_parts.append(part)
    cursor += dur

video = CompositeVideoClip(final_parts, size=(1280,720)).set_duration(audio.duration)
final = video.set_audio(audio)
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')

create_thumbnail(topic)
print("DONE main.py")
