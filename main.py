import os, subprocess
from voice import make_voiceover
from PIL import Image, ImageDraw

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

def make_images_and_video():
    # Make 1 image for video background
    img = Image.new('RGB', (1280, 720), (18,18,18))
    d = ImageDraw.Draw(img)
    d.rectangle([(40,40),(1240,680)], outline=(255,200,0), width=6)
    d.text((80,300), "GameVault - Free Fire Story", fill=(255,255,255))
    d.text((80,380), "Auto Agent Video", fill=(255,200,0))
    img.save("bg.jpg")
    # Use ffmpeg to make video from image + audio (no moviepy needed)
    cmd = 'ffmpeg -y -loop 1 -i bg.jpg -i gamevault_final.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest final_video.mp4'
    subprocess.run(cmd, shell=True)
    print("FINAL VIDEO READY - No Bhag spoken!")

if __name__ == "__main__":
    s = make_final_script()
    print(f"Words: {len(s.split())}")
    make_voiceover(s)
    make_images_and_video()
