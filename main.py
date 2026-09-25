import os, requests, random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, ColorClip
from gtts import gTTS

PEXELS_KEY = os.getenv("PEXELS_KEY")
print(f"KEY STATUS: {bool(PEXELS_KEY)}")

STORY = [
    ("Free Fire ki shuruat 2017 me hui thi", "battle royale parachute"),
    ("Garena ne is game ko banaya", "game developer coding"),
    ("India me 2019 me ye sabse popular hua", "indian gamer headset"),
    ("DJ Alok sabka favourite character bana", "dj concert lights"),
    ("Aaj crore log Free Fire khelte hai", "esports stadium crowd")
]

def download_pexels(query):
    if not PEXELS_KEY:
        print("No PEXELS_KEY!")
        return None
    try:
        headers = {"Authorization": PEXELS_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=5&orientation=portrait"
        r = requests.get(url, headers=headers, timeout=20)
        data = r.json()
        if not data.get('videos'):
            print(f"No videos for {query}")
            return None
        video_link = random.choice(data['videos'])['video_files'][0]['link']
        fname = f"clip_{random.randint(1000,9999)}.mp4"
        print(f"Downloading {query}...")
        with requests.get(video_link, stream=True, timeout=40) as d:
            with open(fname, 'wb') as f:
                for chunk in d.iter_content(1024*1024):
                    f.write(chunk)
        return fname
    except Exception as e:
        print(f"Pexels Error: {e}")
        return None

final_clips = []
for text, q in STORY:
    print(f"\nSCENE: {text}")
    path = download_pexels(q)

    if path and os.path.exists(path):
        try:
            clip = VideoFileClip(path).resize((1080,1920))
            if clip.duration > 5:
                clip = clip.subclip(0,5)
        except:
            clip = ColorClip((1080,1920), color=(20,20,60), duration=4)
    else:
        clip = ColorClip((1080,1920), color=(20,20,60), duration=4)

    # Audio
    audio_file = f"aud_{random.randint(1000,9999)}.mp3"
    try:
        gTTS(text=text, lang='hi').save(audio_file)
        audio = AudioFileClip(audio_file)
        clip = clip.set_duration(audio.duration).set_audio(audio)
    except Exception as e:
        print(f"TTS fail: {e}")
        clip = clip.set_duration(4)

    final_clips.append(clip)

print("Combining...")
final = concatenate_videoclips(final_clips)
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("DONE - final_video.mp4 created!")
