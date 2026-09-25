import os
import random
import requests
from moviepy.editor import *
import moviepy.video.fx as vfx
import moviepy.audio.fx as afx
from gtts import gTTS

# === CONFIG ===
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
TOPIC = "Why you can't stop gaming at 2AM"

# 1. SCRIPT - Fast, punchy Hindi (no slow lines)
script_text = """रात के दो बज रहे हैं। बाहर सन्नाटा है।
तुम्हारी आँखें जल रही हैं। पर तुम रुक नहीं रहे।
क्यों? क्योंकि ये सिर्फ गेम नहीं है।
ये dopamine का जाल है। हर win पर तुम्हारा दिमाग कहता है - एक और मैच।
और तुम फँस जाते हो। Game तुम्हें नहीं, तुम Game को खेल रहे हो।"""

# 2. VOICE - Fast natural Hindi
print("Generating voice...")
tts = gTTS(text=script_text, lang='hi', slow=False)
tts.save("voice.mp3")
audio = AudioFileClip("voice.mp3")
audio = audio.fx(afx.audio_normalize).fx(afx.audio_fadeout, 0.5)
audio = audio.fx(vfx.speedx, 1.28) # <-- FAST VOICE FIX (1.28x)
print(f"Voice duration: {audio.duration}")

# 3. CLIPS - High energy gameplay search
search_terms = [
    "valorant gameplay",
    "fortnite montage",
    "gta 5 gameplay",
    "cyberpunk neon city",
    "esports crowd",
    "rgb gaming keyboard fast"
]

headers = {"Authorization": PEXELS_API_KEY}
video_clips = []

for term in search_terms:
    print(f"Searching: {term}")
    url = f"https://api.pexels.com/videos/search?query={term}&per_page=3&orientation=landscape"
    r = requests.get(url, headers=headers).json()
    for v in r.get('videos', []):
        # Get 720p link
        link = [f for f in v['video_files'] if f['width']==1280][0]['link']
        clip_path = f"clip_{len(video_clips)}.mp4"
        open(clip_path, 'wb').write(requests.get(link).content)

        # FAST CUT + ZOOM EFFECT
        clip = VideoFileClip(clip_path).subclip(0, 1.8) # Only 1.8 sec = not boring
        clip = clip.resize(height=720)
        # Zoom in effect
        clip = clip.fx(vfx.resize, lambda t: 1 + 0.15*t)
        clip = clip.set_position('center').on_color(size=(1280,720), color=(0,0,0))
        video_clips.append(clip)
        if len(video_clips) >= 15:
            break
    if len(video_clips) >= 15:
        break

# 4. BUILD TIMELINE - Repeat clips to match audio
final_clips = []
current_time = 0
while current_time < audio.duration:
    c = random.choice(video_clips)
    final_clips.append(c.set_start(current_time))
    current_time += c.duration

final = CompositeVideoClip(final_clips, size=(1280,720))
final = final.set_duration(audio.duration)
final = final.set_audio(audio)

# 5. EXPORT - Compressed 30MB
print("Exporting final_video.mp4...")
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac', bitrate="1000k", preset='ultrafast')
print("DONE - final_video.mp4 ready")
