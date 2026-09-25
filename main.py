import os, requests, random
from gtts import gTTS
from moviepy.editor import *

PEXELS_KEY = os.getenv("PEXELS_API_KEY") or os.getenv("PEXELS_KEY") or os.getenv("PEXELS_API")
GROQ_KEY = os.getenv("GROQ_API_KEY")

BACKUP_SCRIPTS = [
    "Did you know GTA 5 cost 265 million dollars to make? That's more than most Hollywood movies! It made that back in just 3 days!",
    "Minecraft's world is literally infinite. It would take you 82 years to walk to the end if you never stopped. And there are still secrets no one found!",
    "In PUBG, the pan can actually block bullets. It's the most OP item in the game and pros always keep it!",
    "Free Fire was made in just 8 months but made over 1 billion dollars. The fastest billion dollar game ever made!"
]

def get_script():
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_KEY)
        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user","content":"Write a 25 second viral gaming fact, 70 words max, start with a hook, no intro. Just fact."}],
            max_tokens=150
        )
        text = res.choices[0].message.content.strip()
        print(f"GROQ SCRIPT: {text}")
        if len(text) > 20:
            return text
    except Exception as e:
        print(f"Groq failed: {e}, using backup")
    return random.choice(BACKUP_SCRIPTS)

def make_voice(text):
    tts = gTTS(text=text, lang='en', tld='com')
    tts.save("voice.mp3")
    print("voice.mp3 created")

def download_pexels():
    try:
        headers = {"Authorization": PEXELS_KEY}
        url = "https://api.pexels.com/videos/search?query=gaming+gameplay&per_page=3&orientation=landscape"
        r = requests.get(url, headers=headers, timeout=15)
        clips = []
        for i, v in enumerate(r.json().get("videos", [])[:2]):
            link = v["video_files"][0]["link"]
            path = f"clip{i}.mp4"
            with open(path, "wb") as f:
                f.write(requests.get(link, timeout=20).content)
            clips.append(path)
        print(f"Got {len(clips)} clips")
        return clips
    except Exception as e:
        print(f"Pexels failed: {e}")
        return []

def make_video():
    text = get_script()
    make_voice(text)

    with open("title.txt","w",encoding="utf-8") as f:
        f.write(text[:80] + " #shorts")
    with open("description.txt","w",encoding="utf-8") as f:
        f.write(text + "\n\n#gaming #shorts #facts #gta #freefire #pubg")

    audio = AudioFileClip("voice.mp3")
    dur = audio.duration
    print(f"Audio duration: {dur}")

    clip_files = download_pexels()

    if clip_files:
        vclips = []
        for cf in clip_files:
            try:
                c = VideoFileClip(cf).without_audio().resize(height=720)
                vclips.append(c)
            except:
                pass
        if vclips:
            visual = concatenate_videoclips(vclips).set_duration(dur).resize((1280,720))
        else:
            visual = ColorClip(size=(1280,720), color=(10,10,25), duration=dur)
    else:
        visual = ColorClip(size=(1280,720), color=(10,10,25), duration=dur)

    visual = visual.set_audio(audio)

    # Big viral caption
    txt = TextClip(text, fontsize=42, color='white', method='caption', size=(1100, None), stroke_color='black', stroke_width=3, font='Arial-Bold').set_duration(dur).set_position('center')

    final = CompositeVideoClip([visual, txt])
    final.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("FINAL VIDEO DONE")

if __name__ == "__main__":
    make_video()
