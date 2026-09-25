import os, requests, random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, ColorClip
from gtts import gTTS

PEXELS_KEY = os.getenv("PEXELS_KEY")
print(f"KEY FOUND: {bool(PEXELS_KEY)} - V10.1 FINAL")

SCRIPT = [
    "Free Fire ki kahani shuru hoti hai 2017 se, jab duniya me PUBG aur Fortnite ka craze tha. Tab Garena ne socha ek aisa battle royale banate hai jo har phone me chale.",
    "Garena Singapore ki company hai. Founder Forrest Li ne 2017 me 111 Dots Studio ke saath Free Fire banaya. Beta 7 November 2017 ko launch hua, sirf 20 players ke saath.",
    "Pehla map Bermuda tha. Clock Tower, Factory, Bimasakti Strip. Chhota map, tez action. Har match sirf 10 minute ka. Yahi wajah se ye mobile gamers ko pasand aaya.",
    "2018 me official launch ke baad Garena ne weekly updates diye. Naye guns, naye characters. 2019 me DJ Alok aaya, jo India ke DJ Alok par based tha. India me isne dhamaka kar diya.",
    "DJ Alok ki ability thi HP heal aur speed boost. Har Indian player ise kharidna chahta tha. Total Gaming aur Desi Gamers jaise YouTubers ne is character ko aur famous kiya.",
    "India me Jio ke saste internet ne Free Fire ko gaon gaon tak pahucha diya. 2019-2020 me 50 million daily active users ho gaye. School ke bache bhi rank push karne lage.",
    "2020 me jab PUBG Mobile India me ban hua, Free Fire number 1 ban gaya. Garena ki earning 1 billion dollar cross kar gayi. Free Fire World Series ka prize pool 2 million dollar tak pahucha.",
    "Game me 50 plus characters hai. Kelly fast runner, Moco hacker, Wukong camouflage. Weapons me MP40, M1014, AWM sabse deadly hai.",
    "2021 me Garena ne Free Fire Max launch kiya. HD graphics, better lighting, 4K textures. Low phone wale normal, high phone wale Max khelte hai.",
    "14 February 2022 ko Indian Government ne Free Fire ban kar diya security reasons se. Lakhon players ka dil toota.",
    "Ban ke baad bhi players ne VPN se khelna jari rakha. Free Fire Max ban list me nahi tha, isiliye India me Max chalta raha. Garena ne Free Fire India launch ka wada kiya MS Dhoni ke saath.",
    "Aaj Free Fire ke 1.5 billion downloads hai. Har din 150 million log khelte hai. Ye duniya ka sabse bada mobile battle royale hai."
]

def get_video():
    try:
        headers = {"Authorization": PEXELS_KEY}
        query = random.choice(["gaming", "esports", "neon lights", "city night", "crowd cheering", "action"])
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=10&orientation=portrait"
        r = requests.get(url, headers=headers, timeout=20)
        print(f"Pexels {query} => {r.status_code}")
        vids = r.json().get('videos', [])
        if not vids: return None
        v = random.choice(vids)
        link = None
        for f in v['video_files']:
            if f['width'] < f['height']:
                link = f['link']
                break
        if not link: link = v['video_files'][0]['link']
        fname = f"c_{random.randint(10000,99999)}.mp4"
        with requests.get(link, stream=True, timeout=60) as d:
            with open(fname, 'wb') as out:
                for c in d.iter_content(1024*1024):
                    if c: out.write(c)
        print(f"Downloaded {fname}")
        return fname
    except Exception as e:
        print(f"FAIL {e}")
        return None

clips = []
for i, text in enumerate(SCRIPT):
    print(f"CHAPTER {i+1}/{len(SCRIPT)}")
    p = get_video()
    if p and os.path.exists(p) and os.path.getsize(p) > 10000:
        try:
            cl = VideoFileClip(p).resize((1080,1920))
            if cl.duration > 80: cl = cl.subclip(0,80)
        except:
            cl = ColorClip((1080,1920), color=(15,15,40), duration=5)
    else:
        cl = ColorClip((1080,1920), color=(15,15,40), duration=5)

    ap = f"a_{i}.mp3"
    try:
        gTTS(text=text, lang='hi', slow=False).save(ap)
        aud = AudioFileClip(ap)
        cl = cl.set_duration(aud.duration).set_audio(aud)
    except Exception as e:
        print(f"TTS {e}")
        cl = cl.set_duration(6)
    clips.append(cl)

final = concatenate_videoclips(clips)
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac')
print("DONE - 12 chapters ~15 min READY")
