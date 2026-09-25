import os, requests, asyncio
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.editor import *
import edge_tts

PEXELS_KEY = os.getenv("PEXELS_KEY")

SCRIPT = """
सोचो, रात के दो बज रहे हैं। बाहर सन्नाटा है। तुम्हारी आँखें जल रही हैं,
तुमने शाम से कुछ नहीं खाया, तुम्हारी माँ तीन बार तुम्हें बुला चुकी है।
लेकिन तुम कंट्रोलर नहीं छोड़ सकते। क्यों? क्योंकि तुम्हें लगता है, बस एक और मिशन।
लेकिन सच कुछ और है। ये गेम तुम्हें खेल रहा है।

नमस्कार, आप देख रहे हैं गेम वॉल्ट, और आज हम खोलने जा रहे हैं वीडियो गेम्स का सबसे बड़ा काला सच।

क्या आपने सोचा है, फ्री गेम्स फ्री क्यों हैं? दुनिया में पानी की बोतल भी फ्री नहीं, तो पाँच सौ करोड़ का गेम फ्री कैसे?
जवाब है लत। दो हजार पाँच में बड़ी कंपनियों ने कैसीनो के साइकोलॉजिस्ट हायर किए। वही लोग जो जुए की मशीन बनाते हैं।
जब आप किल करते हैं, जो चमक और आवाज आती है, वो कैसीनो के सिक्के जैसी है, ताकि आपका दिमाग खुश हो और आप और खेलो।

दूसरा धोखा है ग्राफिक्स। आपको लगता है ग्राफिक्स मजे के लिए बेहतर हो रहे हैं? नहीं।
ग्राफिक्स बेहतर हो रहे हैं ताकि असली जिंदगी बदसूरत लगे। गेम में सूरज परफेक्ट है, असल में गर्मी और ट्रैफिक।
इसे कहते हैं विजुअल ट्रैप।

हर गेम का हीरो अकेला लड़का क्यों होता है? जिसे दुनिया नहीं समझती। क्योंकि ये आपकी कहानी है।
आप गेम में अपनी अधूरी जिंदगी पूरी करते हैं।

अब सबसे खतरनाक सच, फ्री टू प्ले। एक आम गेमर अपनी जिंदगी में फ्री गेम पर अस्सी हजार से ज्यादा खर्च करता है।
एक स्किन दो हजार, एक गन पाँच हजार, बैटल पास ग्यारह सौ। बच्चा बटन दबाता है, पापा का पैसा कटता है।
कंपनियां इसे माइक्रोट्रांजैक्शन कहती हैं, मैं इसे डिजिटल जुआ कहता हूँ।

और ई-स्पोर्ट्स? सोलह साल के बच्चे चौदह घंटे प्रैक्टिस करते हैं। बाईस साल में करियर खत्म, हाथ काँपते हैं, आँखें खराब।
कॉन्ट्रैक्ट ऐसा कि छोड़ नहीं सकते। ये स्पोर्ट है या गुलामी?

और अब भविष्य, आर्टिफिशियल इंटेलिजेंस। अगले दो साल में गेम आपको पढ़ेगा।
आप कब बोर हो, कब गुस्सा हो, कब पैसे खर्च करने को तैयार हो। गेम खुद को बदल देगा ताकि आप एग्जिट बटन कभी ना दबाओ।

तो सवाल है, क्या आप गेमर हैं? या आप प्रोडक्ट हैं? आपका समय, आपका ध्यान, यही उनका पैसा है।
अगर इसने आपको सोचने पर मजबूर किया, तो इसे उस दोस्त को भेजो जो रात भर खेलता है।
आप देख रहे थे गेम वॉल्ट।
"""

async def make_voice():
    try:
        print("Trying MALE MadhurNeural...")
        comm = edge_tts.Communicate(SCRIPT, "hi-IN-MadhurNeural", rate="-5%", pitch="+0Hz", volume="+20%")
        await comm.save("voice.mp3")
        print("MALE voice OK")
    except Exception as e:
        print(f"Edge blocked {e}, using natural fallback")
        from gtts import gTTS
        gTTS(text=SCRIPT, lang='hi', slow=False).save("voice_raw.mp3")
        a = AudioFileClip("voice_raw.mp3")
        a = a.fx(vfx.speedx, 0.88) # slower = more natural, less robotic
        a.write_audiofile("voice.mp3")

asyncio.run(make_voice())
audio = AudioFileClip("voice.mp3")
print(f"Duration {audio.duration/60:.1f} mins")

def dl(q,n):
    headers={"Authorization":PEXELS_KEY}
    url=f"https://api.pexels.com/videos/search?query={q}&per_page=12&orientation=landscape"
    files=[]
    try:
        j=requests.get(url,headers=headers,timeout=20).json()
        for v in j.get("videos",[])[:n]:
            link=v["video_files"][0]["link"]
            fn=f"{q[:3]}_{len(files)}.mp4"
            open(fn,'wb').write(requests.get(link,timeout=30).content)
            files.append(fn)
    except: pass
    return files

allf=[]
for q in ["gaming dark room","video game controller","esports tournament","robot ai future","money credit card"]:
    allf.extend(dl(q,5))

clips=[]
total=0
idx=0
while total < audio.duration and allf:
    f=allf[idx % len(allf)]
    try:
        c=VideoFileClip(f).without_audio().resize((1280,720))
        dur=min(4, c.duration, audio.duration-total)
        clips.append(c.subclip(0,dur))
        total+=dur
    except: pass
    idx+=1

final=concatenate_videoclips(clips,method="compose").set_audio(audio)
final.write_videofile("final_video.mp4",fps=24,codec='libx264',audio_codec='aac',bitrate="1000k",preset='ultrafast')
