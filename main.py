import subprocess, requests, urllib.parse, os
from voice import make_voiceover
from PIL import Image, ImageDraw, ImageFont

def make_script():
    return """दोस्तों गेमवॉल्ट पर आपका स्वागत है। आज की इस धमाकेदार वीडियो में हम बात करने वाले हैं फ्री फायर की पूरी सच्ची कहानी के बारे में।
साल दो हजार सत्रह की बात है। भारत में ज्यादातर लोगों के पास कम स्टोरेज वाले फोन थे। पबजी जैसा गेम दो जीबी का था। तभी गरीना कंपनी ने सोचा कि क्यों ना एक ऐसा गेम बनाया जाए जो सिर्फ पाँच सौ एमबी का हो।
जब फ्री फायर इंडिया में लॉन्च हुआ तो सबसे पहले टोटल गेमिंग यानी अज्जू भाई ने इस पर वीडियो बनाई। एक ही रात में लाखों लोगों ने इस गेम को डाउनलोड कर लिया।
दोस्तों फ्री फायर का सबसे बड़ा जादू था इसका साइज। सिर्फ पाँच सौ एमबी। हर जगह ये गेम चलता था।
इस गेम में अलग अलग कैरेक्टर थे जैसे आलोक डीजे। भारतीय प्लेयर्स को आलोक सबसे ज्यादा पसंद था।
धीरे धीरे फ्री फायर ने इंडिया में बड़े बड़े टूर्नामेंट शुरू किए। पचास लाख रुपये का इनाम। ये सिर्फ गेम नहीं बल्कि करियर बन गया था।
फिर आया दो हजार बाईस का वो काला दिन जब सरकार ने इस गेम को बैन कर दिया। पूरे भारत के गेमर्स का दिल टूट गया।
बैन के एक साल बाद फ्री फायर फिर से लौटा एक नए नाम के साथ। फ्री फायर इंडिया। डाउनलोड एक करोड़ से पार हो गया सिर्फ एक हफ्ते में।
आज फ्री फायर भारत का नंबर वन बैटल रॉयल गेम है। हर दिन लाखों लोग इसे खेलते हैं। नारनौल, हिसार, जयपुर जैसे छोटे शहरों में भी इसके टूर्नामेंट होते हैं।
तो दोस्तों ये थी फ्री फायर की पूरी कहानी। गेमवॉल्ट चैनल को सब्सक्राइब करना मत भूलना। जय हिंद जय भारत।""".strip()

def download_real_freefire_images():
    prompts = [
        "Free Fire Bermuda map parachute landing battle royale, mobile gaming 500MB lightweight, vibrant comic style",
        "Indian gamer youtuber Total Gaming Ajju Bhai style, gaming room headphones, streaming Free Fire",
        "DJ Alok Free Fire character healing music aura, concert, game character",
        "Free Fire esports tournament India trophy 50 lakh prize, stadium crowd cheering",
        "Free Fire India comeback celebration Indian flag, 1 crore downloads, happy gamers"
    ]
    for i, p in enumerate(prompts):
        encoded = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&nologo=true&model=flux&seed={i+100}"
        print(f"Downloading REAL visual {i+1}: {p[:30]}...")
        try:
            r = requests.get(url, timeout=60)
            open(f"scene_{i}.jpg","wb").write(r.content)
            # Add big text overlay on REAL image
            img = Image.open(f"scene_{i}.jpg").convert("RGB")
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 58)
            except:
                font = ImageFont.load_default()
            titles = ["500MB KA JADU - 2017","AJJU BHAI - TOTAL GAMING","DJ ALOK - FAV CHARACTER","TOURNAMENT 50 LAKH","FREE FIRE INDIA IS BACK"]
            draw.text((40, 580), titles[i], fill=(255,255,0), font=font, stroke_width=4, stroke_fill=(0,0,0))
            img.save(f"scene_{i}.jpg", quality=90)
        except Exception as e:
            print(f"Failed {i}: {e}, using backup")
            # fallback colored if fails
            Image.new('RGB',(1280,720),(20,40,120)).save(f"scene_{i}.jpg")

def make_video():
    cmd = """ffmpeg -y -loop 1 -t 8 -i scene_0.jpg -loop 1 -t 8 -i scene_1.jpg -loop 1 -t 8 -i scene_2.jpg -loop 1 -t 8 -i scene_3.jpg -loop 1 -t 8 -i scene_4.jpg -i gamevault_final.mp3 -filter_complex "[0:v]scale=1280:720,zoompan=z='min(zoom+0.0015,1.35)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v0]; [1:v]scale=1280:720,zoompan=z='min(zoom+0.0015,1.35)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v1]; [2:v]scale=1280:720,zoompan=z='min(zoom+0.0015,1.35)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v2]; [3:v]scale=1280:720,zoompan=z='min(zoom+0.0015,1.35)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v3]; [4:v]scale=1280:720,zoompan=z='min(zoom+0.0015,1.35)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v4]; [v0][v1][v2][v3][v4]concat=n=5:v=1:a=0[v]" -map "[v]" -map 5:a -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest -r 30 final_video.mp4"""
    subprocess.run(cmd, shell=True, executable='/bin/bash')
    print("V7 REAL VISUALS VIDEO READY!")

if __name__ == "__main__":
    make_voiceover(make_script())
    download_real_freefire_images()
    make_video()
