import os, requests, random, time
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip
from gtts import gTTS

PEXELS_KEY = os.getenv("PEXELS_KEY")
print(f"🔑 PEXELS_KEY found: {bool(PEXELS_KEY)}")

# V8.1 SMART SEARCH - matches Free Fire history story
STORY_LINES = [
    ("Free Fire ki shuruat 2017 me hui thi", "battle royale parachute island"),
    ("Garena ne is game ko banaya tha", "game developer coding dark"),
    ("India me 2019 me yeh sabse popular hua", "indian gamer headset intense"),
    ("DJ Alok jaisa character sabka favourite bana", "dj gaming lights neon"),
    ("Aaj Free Fire Max crore log khelte hai", "esports stadium crowd fire")
]

def get_pexels_video(query):
    if not PEXELS_KEY:
        return None
    try:
        headers = {"Authorization": PEXELS_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=3&orientation=portrait&size=medium"
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        if data.get('videos'):
            video_url = random.choice(data['videos'])['video_files'][0]['link']
            print(f"✅ Found: {query} -> {video_url[:50]}")
            # download
            filename = f"clip_{int(time.time())}_{random.randint(1,99)}.mp4"
            with requests.get(video_url, stream=True, timeout=30) as dv:
                with open(filename, 'wb') as f:
                    for chunk in dv.iter_content(1024*1024):
                        f.write(chunk)
            return filename
    except Exception as e:
        print(f"❌ Pexels error {query}: {e}")
    return None

def create_video():
    clips = []
    audio_clips = []

    for i, (text, search_q) in enumerate(STORY_LINES):
        print(f"\n🎬 Scene {i+1}: {text}")

        # 1. Get real video
        v_path = get_pexels_video(search_q)
        if not v_path:
            print("Fallback color clip")
            from moviepy.editor import ColorClip
            v_path = None
            clip = ColorClip(size=(1080,1920), color=(10,10,40), duration=3)
        else:
            clip = VideoFileClip(v_path).subclip(0, 3).resize((1080,1920))

        # 2. TTS Hindi
        tts = gTTS(text=text, lang='hi', slow=False)
        audio_path = f"audio_{i}.mp3"
        tts.save(audio_path)

        # 3. Sync duration to audio
        audio = AudioFileClip(audio_path)
        clip = clip.set_duration(audio.duration).set_audio(audio)

        # 4. Add text
        txt = TextClip(text, fontsize=60, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2, method='caption', size=(900, None)).set_duration(audio.duration).set_position(('center', 1400))
        final_clip = CompositeVideoClip([clip, txt])

        clips.append(final_clip)

    # Combine
    final = concatenate_videoclips(clips)
    final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("🎉 final_video.mp4 READY - Real Pexels V8.1!")

if __name__ == "__main__":
    create_video()
