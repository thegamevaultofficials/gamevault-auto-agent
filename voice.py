import asyncio
import edge_tts

# MALE - Deep, Attractive, Suspense voice for GameVault
VOICE = "en-IN-PrabhatNeural"
RATE = "-6%"
PITCH = "-2Hz"

async def _make_mp3(text, output="voiceover.mp3"):
    # Add suspense pauses for retention
    text = text.replace(". ", " ... ")
    text = text.replace("! ", "! ... ")
    text = text.replace("? ", "? ... ")
    text = text.replace(", ", ", ... ")
    
    communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(output)
    print(f"✅ Voiceover saved: {output} with MALE voice {VOICE}")
    return output

def make_voiceover(full_script, output="voiceover.mp3"):
    text_to_speak = full_script[:15000]  # ~20 mins max
    print("🎙️ Creating MALE Hinglish voiceover for 15-20 min video...")
    asyncio.run(_make_mp3(text_to_speak, output))
    return output

if __name__ == "__main__":
    test = "Doston! Aaj hum baat karenge Free Fire ke rise ke baare mein. Kaise 500MB ke is game ne PUBG ko takkar di! Ruko... kahani abhi baaki hai."
    make_voiceover(test)
