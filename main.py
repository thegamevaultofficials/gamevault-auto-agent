import os, requests, random
import PIL.Image
# Fix for Pillow 9/10 compatibility
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import *
from gtts import gTTS

PEXELS_KEY = os.getenv("PEXELS_KEY")
TOPIC = "video games gaming"

# Hindi script - 15 min
SCRIPT = """
Doston, kya aapne kabhi socha hai video games ka asli sach kya hai?
Aaj hum baat karenge gaming ki duniya ke top 5 secrets ke baare mein.
Pehla secret, graphics ka jaal. Dusra, story ka addiction. Teesra...
"""

def get_pexels_clips():
    headers = {"Authorization": PEXELS_KEY}
    url = f"https://api.pexels.com/videos/search?query={TOPIC}&per_page=10&orientation=landscape"
    try:
        r = requests.get(url, headers=headers, timeout=20)
        print("PEXELS RESPONSE:", r.status_code)
        data = r.json()
        videos = data.get("videos", [])
        clips = []
        for v in videos[:5]:
            # get best mp4 file
            files = sorted(v["video_files"], key=lambda x: x["width"], reverse=True)
            mp4_url = files[0]["link"]
            filename = f"clip_{len(clips)}.mp4"
            print(f"Downloading {mp4_url}")
            with open(filename, 'wb') as f:
                f.write(requests.get(mp4_url, timeout=30).content)
            clips.append(filename)
        return clips
    except Exception as e:
        print(f"PEXELS FAILED: {e}")
        return []

# 1. Voice - ORIGINAL Hindi voice you liked
print("Making Hindi voice...")
tts = gTTS(text=SCRIPT, lang='hi', slow=False)
tts.save("voice.mp3")

# 2. Visuals - REAL Pexels
clip_files = get_pexels_clips()

if not clip_files:
    print("WARNING: No Pexels clips, using backup search")
    # second try with simple query
    TOPIC = "gaming"
    clip_files = get_pexels_clips()

# 3. Edit
audio = AudioFileClip("voice.mp3")
duration = audio.duration
print(f"Audio duration: {duration}")

video_clips = []
if clip_files:
    for cf in clip_files:
        vc = VideoFileClip(cf).without_audio().resize(height=720).subclip(0, duration/len(clip_files))
        video_clips.append(vc)
    final = concatenate_videoclips(video_clips).set_duration(duration).set_audio(audio)
else:
    # Last fallback - still not blue, use ColorClip + Text but will not happen if PEXELS_KEY is set
    print("STILL NO CLIPS - Check PEXELS_KEY secret!")
    final = ColorClip(size=(1280,720), color=(20,20,20), duration=duration).set_audio(audio)

final.write_videofile("final_video.mp4", fps=24)
print("DONE final_video.mp4 ready")
