import os, requests, random
from groq import Groq
from gtts import gTTS
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

PEXELS_KEY = os.getenv("PEXELS_API_KEY") or os.getenv("PEXELS_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

def get_script():
    client = Groq(api_key=GROQ_KEY)
    prompt = "Write a 30 second viral gaming fact script, 80 words max, hook first. No intro like 'hey guys'. Just fact. Example: GTA 5... Single paragraph only."
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}],
        max_tokens=200
    )
    text = res.choices[0].message.content.strip()
    print(f"SCRIPT: {text}")
    return text

def make_voice(text):
    tts = gTTS(text=text, lang='en', tld='com')
    tts.save("voice.mp3")
    print("Voice saved")

def download_pexels(query="gaming"):
    headers = {"Authorization": PEXELS_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=3&orientation=landscape"
    r = requests.get(url, headers=headers, timeout=20)
    data = r.json()
    files = []
    for i, v in enumerate(data.get("videos",[])[:3]):
        video_url = v["video_files"][0]["link"]
        path = f"clip{i}.mp4"
        with open(path,"wb") as f:
            f.write(requests.get(video_url, timeout=30).content)
        files.append(path)
        print(f"Downloaded {path}")
    if not files:
        # fallback: create color clip
        print("NO PEXELS - using color fallback")
    return files

def make_video():
    text = get_script()
    make_voice(text)

    # Save title/desc
    with open("title.txt","w",encoding="utf-8") as f:
        f.write(text[:90] + " | Gaming Facts")
    with open("description.txt","w",encoding="utf-8") as f:
        f.write(text + "\n\n#gaming #facts #gta #shorts")

    clips_files = download_pexels("video game")

    audio = AudioFileClip("voice.mp3")
    duration = audio.duration

    if clips_files:
        video_clips = []
        for cf in clips_files:
            try:
                c = VideoFileClip(cf).without_audio().resize(height=720)
                c = c.subclip(0, min(c.duration, duration/len(clips_files)+1))
                video_clips.append(c)
            except Exception as e:
                print(f"Clip error {e}")
        if video_clips:
            final_visual = concatenate_videoclips(video_clips).subclip(0, duration)
        else:
            final_visual = ColorClip(size=(1280,720), color=(15,15,15), duration=duration)
    else:
        final_visual = ColorClip(size=(1280,720), color=(15,15,15), duration=duration)

    final_visual = final_visual.set_audio(audio)

    # Add text overlay
    txt = TextClip(text, fontsize=50, color='white', method='caption', size=(1000,None), stroke_color='black', stroke_width=2).set_duration(duration).set_position('center')
    final = CompositeVideoClip([final_visual, txt])

    final.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("final_video.mp4 DONE")

if __name__ == "__main__":
    make_video()
