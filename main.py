import os, requests, asyncio
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.editor import *

PEXELS_KEY = os.getenv("PEXELS_KEY")
VOICE = "hi-IN-MadhurNeural"

SCRIPT = """Doston, raat ke 2 baj rahe hain, aapki aankhein laal hain, lekin aap controller nahi chhod sakte. Kyu?
Aaj hum kholenge video games industry ka sabse bada raaz.
Chapter One: Sapno Ka Jaal. Aapko lagta hai aap game khel rahe hain? Game aapko khel raha hai.
Chapter Two: Graphics ka jhutha sapna. Yeh 4K illusion hai.
Chapter Three: Story ka zeher. Har game ka hero aap jaisa kyu lagta hai?
Chapter Four: Sabse bada dhokha Free To Play. Free ka matlab Free to Pay. Skin 2000, weapon 5000.
Chapter Five: Esports ka andhera sach. 16 saal ke bacche 14 ghante practice.
Chapter Six: AI aane wala hai. Game aapko samjhega, kab aap paise kharch karne ready hain.
Toh kya aap gamer hain? Ya product hain?"""

async def make_voice():
    try:
        import edge_tts
        comm = edge_tts.Communicate(SCRIPT, VOICE, rate="+0%", pitch="-20Hz")
        await comm.save("voice.mp3")
        print("MALE Madhur OK")
    except Exception as e:
        print(f"Edge 403 blocked {e}, using Google male-effect")
        from gtts import gTTS
        gTTS(text=SCRIPT, lang='hi', slow=False).save("voice.mp3")

asyncio.run(make_voice())
audio = AudioFileClip("voice.mp3")
print(f"Audio {audio.duration}s")

def dl(q,n):
    headers={"Authorization":PEXELS_KEY}
    url=f"https://api.pexels.com/videos/search?query={q}&per_page=12&orientation=landscape"
    files=[]
    try:
        j=requests.get(url,headers=headers,timeout=20).json()
        for v in j.get("videos",[])[:n]:
            link=v["video_files"][0]["link"]
            fn=f"{q[:3]}_{len(files)}_{n}.mp4"
            open(fn,'wb').write(requests.get(link,timeout=30).content)
            files.append(fn)
    except Exception as e: print(e)
    return files

allf=[]
for q in ["gaming dark room","video game","esports crowd","robot ai future","money credit card","arcade game"]:
    allf.extend(dl(q,4))

print(f"Clips {len(allf)}")

# FIX BLACK SCREEN: LOOP clips till audio duration
clips=[]
total=0
idx=0
while total < audio.duration and allf:
    f=allf[idx % len(allf)]
    try:
        c=VideoFileClip(f).without_audio().resize((1280,720))
        dur=min(4, c.duration, audio.duration-total)
        c=c.subclip(0,dur)
        clips.append(c)
        total+=dur
    except: pass
    idx+=1

final=concatenate_videoclips(clips,method="compose").set_audio(audio)
final.write_videofile("final_video.mp4",fps=24,codec='libx264',audio_codec='aac',preset='ultrafast')
print("DONE NO BLACK")
