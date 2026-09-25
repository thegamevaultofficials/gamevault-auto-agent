import os, random, requests, textwrap
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_script():
    topics = [
        "Top 5 hidden features in GTA 5 that 99% missed",
        "The dark story of Minecraft's Herobrine",
        "5 secret places in BGMI Erangel that pros use",
        "The man who played GTA 5 for 10 years straight",
        "Most expensive gaming setups in the world"
    ]
    topic = random.choice(topics)
    script = f"Did you know {topic}? Number 5 will shock you. Let's start. Number one is insane, number two is hidden by Rockstar, number three pros don't want you to know, number four is a glitch, and number five will blow your mind. Follow for part 2."

    if GROQ_API_KEY:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            prompt = f"Write 120 words viral YouTube Shorts script for '{topic}'. Start with hook, 5 quick facts, energetic."
            data = {"model": "llama-3.3-70b-versatile", "messages": [{"role":"user","content":prompt}]}
            r = requests.post(url, headers=headers, json=data, timeout=30)
            script = r.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Groq fail {e}")
    return topic, script

def create_text_image(text, out_path="text.png"):
    # Creates text image with PIL - never crashes
    W, H = 1280, 250
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # Try to use a bold font
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 55)
    except:
        font = ImageFont.load_default()

    wrapped = textwrap.fill(text, width=30)
    # Draw black stroke
    x, y = 30, 20
    for line in wrapped.split("\n"):
        draw.text((x-2,y-2), line, font=font, fill="black")
        draw.text((x+2,y-2), line, font=font, fill="black")
        draw.text((x-2,y+2), line, font=font, fill="black")
        draw.text((x+2,y+2), line, font=font, fill="black")
        draw.text((x,y), line, font=font, fill="white")
        y += 70
    img.save(out_path)
    return out_path

# --- MAIN ---
topic, script_text = generate_script()
print(f"TOPIC: {topic}")
print(f"SCRIPT: {script_text}")

with open("title.txt","w", encoding="utf-8") as f:
    f.write(topic)

tts = gTTS(text=script_text, lang='en', slow=False)
tts.save("voice.mp3")
audio = AudioFileClip("voice.mp3")
print(f"Audio: {audio.duration}s")

# Get Pexels clips
video_clips = []
headers = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else {}
try:
    query = random.choice(["gaming setup rgb", "esports gaming", "gaming pc neon", "cyberpunk city", "video game controller"])
    print(f"Searching: {query}")
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=landscape"
    r = requests.get(url, headers=headers, timeout=30)
    print(f"Pexels: {r.status_code}")
    for v in r.json().get("videos", [])[:8]:
        best = sorted(v['video_files'], key=lambda x: x['width'], reverse=True)[0]
        tmp = f"temp_{len(video_clips)}.mp4"
        with open(tmp, 'wb') as f:
            f.write(requests.get(best['link'], timeout=20).content)
        # Resize + add slow zoom effect
        base = VideoFileClip(tmp).resize(height=720).crop(width=1280, height=720, x_center=640, y_center=360)
        # Cinematic zoom
        def zoom(t): return 1 + 0.04*t
        clip = base.resize(lambda t: zoom(t))
        video_clips.append(clip)
except Exception as e:
    print(f"Pexels error: {e}")

if len(video_clips) == 0:
    for i in range(6):
        color = (random.randint(20,255), random.randint(20,255), random.randint(20,255))
        video_clips.append(ColorClip((1280,720), color=color, duration=4))

# Build timeline
final_clips = []
cursor = 0
while cursor < audio.duration:
    c = random.choice(video_clips)
    dur = min(3, c.duration)
    start = random.uniform(0, max(0, c.duration-dur))
    part = c.subclip(start, start+dur).set_start(cursor)
    final_clips.append(part)
    cursor += dur

# Base video
video = CompositeVideoClip(final_clips, size=(1280,720)).set_duration(audio.duration)

# Add text image on top
text_png = create_text_image(topic)
txt_clip = ImageClip(text_png, duration=min(5, audio.duration)).set_pos(("center", 0.65), relative=True).set_duration(audio.duration)

final = CompositeVideoClip([video, txt_clip]).set_audio(audio)
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("V2 DONE!")
