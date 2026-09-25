import os, requests, asyncio
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.editor import *

PEXELS_KEY = os.getenv("PEXELS_KEY")
VOICE = "hi-IN-MadhurNeural" # MALE

SCRIPT = """Doston, raat ke 2 baj rahe hain, aapki aankhein laal hain, lekin aap controller nahi chhod sakte. Kyu?
Aaj hum kholenge video games industry ka sabse bada raaz.
Chapter One: Sapno Ka Jaal. Aapko lagta hai aap game khel rahe hain? Galat. Game aapko khel raha hai.
Har saal companies 200 billion dollars kharch karti hain aapko screen se chipkaye rakhne ke liye.
Chapter Two: Graphics ka jhutha sapna. Yeh 4K, 8K, Ray Tracing ek illusion hai, taaki asal zindagi boring lage.
Chapter Three: Story ka zeher. Har game ka hero aap jaisa hi kyu lagta hai? Yeh coincidence nahi hai.
Chapter Four: Sabse bada dhokha - Free To Play. Free ka matlab Free to Pay. Ek skin 2000 rupaye, ek weapon 5000.
Chapter Five: Esports ka andhera sach. 16 saal ke bacche 14 ghante practice, career 22 mein khatam.
Chapter Six: AI aane wala hai. Agle 2 saal mein game aapko samjhega, kab aap paise kharch karne ready hain.
Toh sawal hai, kya aap gamer hain? Ya aap product hain?"""

async def try_edge_male():
    import edge_tts
    comm = edge_tts.Communicate(SCRIPT, VOICE, rate="+0%", pitch="-15Hz")
    await comm.save("voice.mp3")
    print("MALE voice Madhur success")

def make_gtts_male_fallback():
    print("Edge blocked 403, using Google Male-effect fallback...")
    from gtts import gTTS
    gTTS(text=SCRIPT, lang='hi', slow=False).save("voice_raw.mp3")
    # Make female sound male by lowering speed & pitch via moviepy
    a = AudioFileClip("voice_raw.mp3")
    # Slow down 8% = deeper male-like voice
    a = a.fx(vfx.speedx, 0.92)
    a.write_audiofile("voice.mp3")
    print("Fallback MALE-effect voice ready")

# Try edge, if 403 fail -> fallback
try:
    asyncio.run(try_edge_male())
except Exception as e:
    print(f"Edge failed {e} -> fallback")
    make_gtts_male_fallback()

audio = AudioFileClip("voice.mp3")
print(f"Audio {audio.duration/60:.1f} mins")

# Visuals - correct chapter-wise
def dl(query, n):
    headers={"Authorization":PEXELS_KEY}
    url=f"https://api.pexels.com/videos/search?query={query}&per_page=10&orientation=landscape"
    try:
        r=requests.get(url, headers=headers, timeout=20).json()
        files=[]
        for v in r.get("videos",[])[:n]:
            link=v["video_files"][0]["link"]
            fn=f"{query[:4]}_{len(files)}.mp4"
            open(fn,'wb').write(requests.get(link,timeout=30).content)
            files.append(fn)
        return files
    except: return []

queries=["gaming dark room","video game graphics","esports tournament","money credit card","ai future tech"]
allf=[]
for q in queries: allf.extend(dl(q,3))

clips=[]
chunk=audio.duration/max(1,len(allf)) if allf else audio.duration
for f in allf:
    try:
        c=VideoFileClip(f).without_audio().resize((1280,720)).subclip(0,min(chunk,4))
        clips.append(c)
    except: pass

final=concatenate_videoclips(clips,method="compose").set_duration(audio.duration).set_audio(audio) if clips else ColorClip((1280,720),color=(15,15,15),duration=audio.duration).set_audio(audio)
final.write_videofile("final_video.mp4",fps=24,codec='libx264',audio_codec='aac',preset='ultrafast')
print("DONE GREEN")
