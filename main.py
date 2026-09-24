import subprocess
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

def create_gaming_visuals():
    scenes = [
        ("2017 - 500MB KA JADU", "500MB vs 2GB PUBG", (10,30,120)),
        ("AJJU BHAI - TOTAL GAMING", "1M Downloads in 1 Night", (90,10,90)),
        ("DJ ALOK - FAV CHARACTER", "Music Heals HP", (130,70,0)),
        ("TOURNAMENT - 50 LAKH", "Esports Career Start", (0,90,90)),
        ("FREE FIRE INDIA IS BACK", "1 Crore Comeback", (0,110,20)),
    ]
    try:
        f_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        f_mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    except:
        f_big = ImageFont.load_default()
        f_mid = ImageFont.load_default()

    for i, (title, sub, base) in enumerate(scenes):
        # Create gradient background - no white lines
        img = Image.new('RGB', (1280, 720), base)
        draw = ImageDraw.Draw(img)
        # Add darker gradient top to bottom
        for y in range(720):
            r = int(base[0] + y*0.2)
            g = int(base[1] + y*0.1)
            b = int(base[2] + y*0.3)
            draw.line([(0,y),(1280,y)], fill=(min(r,255), min(g,255), min(b,255)))
        # Add gaming controller circle and phone shape
        draw.rounded_rectangle([950, 150, 1200, 550], radius=30, outline=(255,255,0), width=6)
        draw.ellipse([1000, 200, 1150, 350], outline=(0,255,255), width=4)
        # Big Yellow Title with black stroke
        draw.text((50, 200), title, fill=(255, 235, 0), font=f_big, stroke_width=5, stroke_fill=(0,0,0))
        draw.text((55, 310), sub, fill=(255,255,255), font=f_mid, stroke_width=4, stroke_fill=(0,0,0))
        draw.text((50, 650), f"GameVault | Free Fire Story | Scene {i+1}/5", fill=(0,255,255), font=f_mid)
        img.save(f"scene_{i}.jpg", quality=95)
        print(f"Created {title}")

def make_video():
    # Fixed zoom - NO black bar, smooth Ken Burns
    cmd = """ffmpeg -y -loop 1 -t 8 -i scene_0.jpg -loop 1 -t 8 -i scene_1.jpg -loop 1 -t 8 -i scene_2.jpg -loop 1 -t 8 -i scene_3.jpg -loop 1 -t 8 -i scene_4.jpg -i gamevault_final.mp3 -filter_complex "[0:v]scale=1280:720,zoompan=z='min(zoom+0.0012,1.3)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v0]; [1:v]scale=1280:720,zoompan=z='min(zoom+0.0012,1.3)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v1]; [2:v]scale=1280:720,zoompan=z='min(zoom+0.0012,1.3)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v2]; [3:v]scale=1280:720,zoompan=z='min(zoom+0.0012,1.3)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v3]; [4:v]scale=1280:720,zoompan=z='min(zoom+0.0012,1.3)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[v4]; [v0][v1][v2][v3][v4]concat=n=5:v=1:a=0[v]" -map "[v]" -map 5:a -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest -r 30 final_video.mp4"""
    subprocess.run(cmd, shell=True, executable='/bin/bash')
    print("V6 READY - No black bar!")

if __name__ == "__main__":
    s = make_script()
    make_voiceover(s)
    create_gaming_visuals()
    make_video()
