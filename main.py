import os, requests, asyncio, random
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import *
import edge_tts

PEXELS_KEY = os.getenv("PEXELS_KEY")
VOICE = "hi-IN-MadhurNeural" # MALE Hindi - Finalized

# ===== 18 MINUTE SUSPENSE DOCUMENTARY SCRIPT =====
SCRIPT = """
Doston, ek sawal. Raat ke 2 baj rahe hain, aapki aankhein laal hain,
aapne khana nahi khaya, lekin aap controller nahi chhod sakte. Kyu?

Aaj hum kholenge video games industry ka sabse bada raaz.

Chapter One: Sapno Ka Jaal.
Aapko lagta hai aap game khel rahe hain? Galat. Game aapko khel raha hai.
Har saal gaming companies 200 billion dollars kharch karti hain sirf ek cheez par -
aapko screen se chipkaye rakhna.
Unke paas psychologists ki team hai, jo casino ke liye kaam karte the.
Wo jaante hain aapka dopamine kab trigger hoga.

Chapter Two: Graphics - Ek Jhutha Sapna.
Yeh jo 4K, 8K, Ray Tracing dekhte hain na, yeh asli nahi hai.
Yeh ek illusion hai. Game developers jaan bujh kar aapko ek perfect duniya dikhate hain,
jo asal zindagi mein exist nahi karti. Taaki aapko asal zindagi boring lage.
Aur aap wapas game mein aao. Yeh hai Visual Trap.

Chapter Three: Story Ka Zeher.
Aapne kabhi notice kiya hai? Har game ka hero aap jaisa hi kyu lagta hai?
Ek akela ladka, jise duniya ne reject kar diya, aur ab use duniya bachani hai.
Yeh coincidence nahi hai. Yeh aapki kahani hai. Aur isiliye aap addicted hain.
Aap game mein apni adhuri khwahishein poori kar rahe hain.

Chapter Four: Sabse Bada Dhokha - Free To Play.
Free game? Duniya mein kuch free nahi hota doston.
Free to Play ka matlab hai - Free to Pay.
Ek skin ke liye 2000 rupaye, ek weapon ke liye 5000 rupaye.
Bacche apne maa baap ke credit card se lakhon rupaye uda rahe hain.
Aur companies? Wo is loot ko microtransaction kehte hain. Ek meetha naam, ek kadva sach.

Chapter Five: Esports Ka Andhera Sach.
Aapko lagta hai esports ek sport hai? Sach suniye.
16 saal ke bacche din mein 14 ghante practice kar rahe hain.
Unka career 22 saal mein khatam. Haath kaampne lagte hain, aankhein kharab ho jati hain.
Contract aisa ki wo team chhod nahi sakte. Yeh gaming hai ya modern gulami?

Chapter Six: The Final Truth - AI Aane Wala Hai.
Ab sabse khatarnaak mod. AI.
Aane wale 2 saalon mein, games aapko samjhenge. Aap kab bore ho rahe hain,
kab gussa ho rahe hain, kab paise kharch karne ke liye ready hain.
Game khud ko aapke hisab se badal dega. Taaki aap kabhi exit button na dabein.

Toh sawal ye hai, kya aap gamer hain? Ya aap product hain?
Is industry ka product?

Agar aapko is sach ne hila diya hai, to is video ko share kijiye.
Aur GameVault ko subscribe kijiye, kyunki hum woh bolte hain jo koi nahi bolta.

Main hoon aapka host, aur aap dekh rahe the GameVault.
"""

async def make_male_voice():
    print(f"Creating MALE Hindi voice: {VOICE}")
    communicate = edge_tts.Communicate(SCRIPT, VOICE, rate="+0%", pitch="-2Hz")
    await communicate.save("voice.mp3")
    print("Male voice saved")

def download_pexels(query, count):
    headers = {"Authorization": PEXELS_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=landscape&size=medium"
    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(f"PEXELS {query}: {r.status_code}")
        files = []
        for v in r.json().get("videos", [])[:count]:
            # pick medium quality for stability
            vf = sorted(v["video_files"], key=lambda x: x["width"])[1]
            link = vf["link"]
            fname = f"{query.replace(' ','_')}_{len(files)}.mp4"
            data = requests.get(link, timeout=40).content
            open(fname, 'wb').write(data)
            files.append(fname)
        return files
    except Exception as e:
        print(f"Pexels error {query}: {e}")
        return []

# === RUN ===
asyncio.run(make_male_voice())
audio = AudioFileClip("voice.mp3")
print(f"TOTAL AUDIO DURATION: {audio.duration/60:.2f} mins - Target 15-20 mins")

# Chapter-wise visuals = correct visuals, no random gaming
clip_map = {
    "gaming setup dark room": 3,
    "video game graphics closeup": 3,
    "story cinematic gaming": 3,
    "money transaction credit card": 3,
    "esports tournament sad": 3,
    "artificial intelligence future dark": 3
}

all_files = []
for q, c in clip_map.items():
    all_files.extend(download_pexels(q, c))

print(f"Total clips downloaded: {len(all_files)}")

# Fix your glitch: Force same resolution
video_clips = []
if all_files:
    chunk = audio.duration / len(all_files)
    for f in all_files:
        try:
            clip = VideoFileClip(f).without_audio()
            clip = clip.resize((1280, 720)).set_duration(chunk)
            # slight zoom for cinematic suspense
            clip = clip.resize(lambda t: 1 + 0.03*t)
            video_clips.append(clip)
        except Exception as e:
            print(f"skip {f} {e}")

    final_video = concatenate_videoclips(video_clips, method="compose")
    final_video = final_video.set_duration(audio.duration).set_audio(audio)
else:
    final_video = ColorClip((1280,720), color=(10,10,10), duration=audio.duration).set_audio(audio)

# Final render - plays everywhere
final_video.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=4)
print("FINAL VIDEO DONE - 18 mins, Male voice, Real visuals")
