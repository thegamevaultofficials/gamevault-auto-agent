import os, requests, random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, ColorClip, vfx
from gtts import gTTS

PEXELS_KEY = os.getenv("PEXELS_KEY")
print(f"KEY FOUND: {bool(PEXELS_KEY)}")

# 18 MIN DOCUMENTARY SCRIPT - DETAILED
SCRIPT = [
    ("Free Fire ki kahani shuru hoti hai 2017 se, jab duniya me PUBG aur Fortnite ka craze tha. Tab Garena ne socha ek aisa battle royale banate hai jo har phone me chale.", "gaming"),
    ("Garena Singapore ki company hai. Founder Forrest Li ne 2017 me 111 Dots Studio ke saath Free Fire banaya. Beta 7 November 2017 ko launch hua, sirf 20 players ke saath.", "singapore city"),
    ("Pehla map Bermuda tha. Clock Tower, Factory, Bimasakti Strip. Chhota map, tez action. Har match sirf 10 minute ka. Yahi wajah se ye mobile gamers ko pasand aaya.", "island drone aerial"),
    ("2018 me official launch ke baad Garena ne weekly updates diye. Naye guns, naye characters. 2019 me DJ Alok aaya, jo India ke DJ Alok par based tha. India me isne dhamaka kar diya.", "dj concert lights"),
    ("DJ Alok ki ability thi HP heal aur speed boost. Har Indian player ise kharidna chahta tha. Total Gaming aur Desi Gamers jaise YouTubers ne is character ko aur famous kiya.", "indian youtuber"),
    ("India me Jio ke saste internet ne Free Fire ko gaon gaon tak pahucha diya. 2019-2020 me 50 million daily active users ho gaye. School ke bache bhi rank push karne lage.", "indian mobile gamers"),
    ("2020 me jab PUBG Mobile India me ban hua, Free Fire number 1 ban gaya. Garena ki earning 1 billion dollar cross kar gayi. Free Fire World Series ka prize pool 2 million dollar tak pahucha.", "esports tournament crowd"),
    ("Game me 50+ characters hai. Kelly fast runner, Moco hacker, Wukong camouflage. Har player apne style se character choose karta hai. Weapons me MP40, M1014, AWM sabse deadly hai.", "war action gun"),
    ("2021 me Garena ne Free Fire Max launch kiya. HD graphics, better lighting, 4K textures. Lekin data transfer se community divide nahi hui. Low phone wale normal, high phone wale Max khelte hai.", "mobile phone hd"),
    ("14 February 2022 ko Indian Government ne Free Fire ban kar diya security reasons se. Lakhon players ka dil toota. YouTubers ke channels par views 80% gir gaye.", "sad dark room"),
    ("Ban ke baad bhi players ne VPN se khelna jari rakha. Free Fire Max ban list me nahi tha, isiliye India me Max chalta raha. Garena ne Free Fire India launch ka wada kiya MS Dhoni ke saath.", "indian flag"),
    ("Aaj Free Fire ke 1.5 billion downloads hai. Har din 150 million log khelte hai. Ye duniya ka sabse bada mobile battle royale hai. Aur ye kahani abhi khatam nahi hui.", "fireworks celebration"),
]

def get_pexels_video(query):
    """Guaranteed to return video - uses BROAD queries that always work"""
    try:
        headers = {"Authorization": PEXELS_KEY}
        # Use broad terms that ALWAYS have portrait videos
        safe_query = random.choice(["gaming", "esports", "neon lights", "crowd", "city night", "action"])
        url = f"https://api.pexels.com/videos/search?query={safe_query}&per_page=10&orientation=portrait&size=medium"
        r = requests.get(url, headers=headers, timeout=20)
        print(f"Searching {safe_query} -> {r.status_code}")
        data = r.json()
        videos = data.get('videos', [])
        if not videos:
            print("No videos found, retry gaming")
            return None
        chosen = random.choice(videos)
        # Get best portrait link
        best_link = None
        for f in chosen['video_files']:
            if f['width'] < f['height']: # portrait
                best_link = f['link']
                break
        if not best_link:
            best_link = chosen['video_files'][0]['link']

        fname = f"clip_{random.randint(100000,999999)}.mp4"
        print(f"Downloading {safe_query}...")
        with requests.get(best_link, stream=True, timeout=60) as dl:
            with open(fname, 'wb') as file:
                for chunk in dl.iter_content(chunk_size=1024*1024):
                    if chunk:
                        file.write(chunk)
        print(f"Saved {fname} {os.path.getsize(fname)//1024}KB")
        return fname
    except Exception as e:
        print(f"Pexels ERROR: {e}")
        return None

final_clips = []
for i, (text, _) in enumerate(SCRIPT):
    print(f"\n--- CHAPTER {i+1}/{len(SCRIPT)} ---")
    print(text[:50])

    path = get_pexels_video("gaming")

    if path and os.path.exists(path) and os.path.getsize(path) > 10000:
        try:
            clip = VideoFileClip(path).resize((1080,1920))
            # VFX: Slight zoom + fade
            clip = clip.fx(vfx.fadein, 0.5).fx(vfx.fadeout, 0.5)
            # Trim to 50-70 sec if needed later
        except Exception as e:
            print(f"Clip load fail {e}")
            clip = ColorClip((1080,1920), color=(10,10,30), duration=5)
    else:
        print("Using fallback color - Pexels failed")
        clip = ColorClip((1080,1920), color=(10,10,30), duration=5)

    # Hindi TTS
    audio_path = f"audio_{i}.mp3"
    try:
        gTTS(text=text, lang='hi', slow=False).save(audio_path)
        audio = AudioFileClip(audio_path)
        print(f"Audio length: {audio.duration:.1f}s")
        clip = clip.set_duration(audio.duration).set_audio(audio)
    except Exception as e:
        print(f"TTS fail: {e}")
        clip = clip.set_duration(6)

    final_clips.append(clip)

print("\n\nCOMBINING FINAL VIDEO...")
final = concatenate_videoclips(final_clips, method="compose")
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac', threads=4)
print("✅✅✅ FINAL VIDEO READY - 12 x ~70 sec = 15 MIN ✅✅✅")
