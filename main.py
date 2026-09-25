import os, random, requests, textwrap
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_long_script():
    topics = [
        "The man who played GTA 5 for 10 years straight - his story",
        "Top 10 darkest secrets hidden in GTA 5 by Rockstar",
        "The complete history of Minecraft Herobrine - full documentary",
        "How Free Fire was banned and destroyed a million careers"
    ]
    topic = random.choice(topics)
    # Default long script if Groq fails
    script = f"""
    Today we explore {topic}. This is a full documentary.
    Part 1: The beginning. It all started in 2013 when GTA 5 launched.
    Part 2: The obsession. He played 14 hours a day for 10 years.
    Part 3: The hidden secrets Rockstar hid inside the game.
    Part 4: What happened to him in the end will shock you.
    Stay till the end for number 1 fact that 99 percent of players missed.
    """ * 15 # makes it long

    if GROQ_API_KEY:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            prompt = f"Write a 900 word engaging YouTube LONG VIDEO documentary script for '{topic}'. Make it 8 sections, storytelling, hook, keep audience till end. No brackets, just narration."
            data = {"model": "llama-3.3-70b-versatile", "messages": [{"role":"user","content":prompt}], "max_tokens": 4000}
            r = requests.post(url, headers=headers, json=data, timeout=60)
            script = r.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Groq fail: {e}")

    return topic, script

def create_text_image(text, out_path="text.png"):
    W, H = 1280, 200
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 50)
    except:
        font = ImageFont.load_default()
    wrapped = textwrap.fill(text, width=35)
    x, y = 30, 20
    for line in wrapped.split("\n")[:3]: # only 3 lines
        draw.text((x-3,y-3), line, font=font, fill="black")
        draw.text((x+3,y+3), line, font=font, fill="black")
        draw.text((x,y), line, font=font, fill="white")
        y += 65
    img.save(out_path)
    return out_path

# --- MAIN ---
topic, script_text = generate_long_script()
print(f"TOPIC: {topic}")
print(f"SCRIPT LENGTH: {len(script_text)} chars")

with open("title.txt","w", encoding="utf-8") as f:
    f.write(topic)

# Long voice - split into parts because gTTS has limit
print("Creating LONG voice...")
parts = [script_text[i:i+4000] for i in range(0, len(script_text), 4000)]
audio_clips = []
for idx, part in enumerate(parts):
    path = f"voice_{idx}.mp3"
    tts = gTTS(text=part, lang='en', slow=False)
    tts.save(path)
    audio_clips.append(AudioFileClip(path))

final_audio = concatenate_audioclips(audio_clips)
final_audio.write_audiofile("voice.mp3")
audio = final_audio
print(f"Final Audio Duration: {audio.duration/60:.2f} minutes")

# Get MANY Pexels clips for long video
video_clips = []
headers = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else {}
try:
    queries = ["gaming setup rgb", "esports gaming", "video game controller", "gaming pc neon", "cyberpunk city night"]
    for q in queries:
        url = f"https://api.pexels.com/videos/search?query={q}&per_page=10&orientation=landscape"
        r = requests.get(url, headers=headers, timeout=30)
        for v in r.json().get("videos", [])[:4]:
            best = sorted(v['video_files'], key=lambda x: x['width'], reverse=True)[0]
            tmp = f"temp_{len(video_clips)}.mp4"
            with open(tmp, 'wb') as f:
                f.write(requests.get(best['link'], timeout=20).content)
            base = VideoFileClip(tmp).resize(height=720).crop(width=1280, height=720, x_center=640, y_center=360)
            video_clips.append(base)
        if len(video_clips) >= 25:
            break
except Exception as e:
    print(f"Pexels error: {e}")

if len(video_clips) < 5:
    for i in range(10):
        video_clips.append(ColorClip((1280,720), color=(20,20,20), duration=5))

# Build timeline for 8-10 min
final_parts = []
cursor = 0
while cursor < audio.duration - 1:
    c = random.choice(video_clips)
    dur = random.uniform(4, 7) # longer cuts for long video
    dur = min(dur, c.duration, audio.duration - cursor)
    if dur < 2:
        break
    start = random.uniform(0, max(0, c.duration-dur))
    part = c.subclip(start, start+dur).set_start(cursor)
    final_parts.append(part)
    cursor += dur

video = CompositeVideoClip(final_parts, size=(1280,720)).set_duration(audio.duration)

# Title stays first 8 seconds only for long video
text_png = create_text_image(topic)
txt_clip = ImageClip(text_png, duration=8).set_pos(("center", 0.75), relative=True).set_start(0)

final = CompositeVideoClip([video, txt_clip]).set_audio(audio)
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("LONG VIDEO DONE!")
