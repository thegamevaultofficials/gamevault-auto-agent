import os, subprocess, requests
from voice import make_voiceover
from PIL import Image

def make_final_script():
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

def download_gaming_visuals():
    urls = [
        "https://picsum.photos/seed/ff1/1280/720",
        "https://picsum.photos/seed/ff2/1280/720",
        "https://picsum.photos/seed/ff3/1280/720",
        "https://picsum.photos/seed/ff4/1280/720",
        "https://picsum.photos/seed/ff5/1280/720"
    ]
    for i, url in enumerate(urls):
        try:
            r = requests.get(url, timeout=20)
            open(f"scene_{i}.jpg","wb").write(r.content)
            print(f"Downloaded visual {i}")
        except:
            Image.new('RGB',(1280,720),(i*40,100,200)).save(f"scene_{i}.jpg")

def make_video_with_animation():
    cmd = """ffmpeg -y -loop 1 -t 8 -i scene_0.jpg -loop 1 -t 8 -i scene_1.jpg -loop 1 -t 8 -i scene_2.jpg -loop 1 -t 8 -i scene_3.jpg -loop 1 -t 8 -i scene_4.jpg -i gamevault_final.mp3 -filter_complex "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(pzoom+0.0015,1.5)':s=1280x720:d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v0]; [1:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(pzoom+0.0015,1.5)':s=1280x720:d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v1]; [2:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(pzoom+0.0015,1.5)':s=1280x720:d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v2]; [3:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(pzoom+0.0015,1.5)':s=1280x720:d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v3]; [4:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(pzoom+0.0015,1.5)':s=1280x720:d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'[v4]; [v0][v1][v2][v3][v4]concat=n=5:v=1:a=0[v]" -map "[v]" -map 5:a -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest final_video.mp4"""
    subprocess.run(cmd, shell=True, executable='/bin/bash')
    print("ANIMATED VIDEO READY!")

if __name__ == "__main__":
    s = make_final_script()
    make_voiceover(s)
    download_gaming_visuals()
    make_video_with_animation()
