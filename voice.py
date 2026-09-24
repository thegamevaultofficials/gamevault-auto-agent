import asyncio
import edge_tts

# This is your permanent Hinglish voice - Indian female gamer style
VOICE = "hi-IN-SwaraNeural"
RATE = "+8%"

async def _make_mp3(text, output="voiceover.mp3"):
    # Split 2800 words into parts because TTS limit
    # For 20 min video = ~2800 words = 3 parts
    communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE)
    await communicate.save(output)
    print(f"✅ Voiceover saved: {output}")
    return output

def make_voiceover(full_script, output="voiceover.mp3"):
    # Clean Hinglish for voice
    # Edge TTS handles Hindi+English mix automatically
    text_to_speak = full_script[:15000]  # ~20 mins max
    print("🎙️ Creating Hinglish voiceover for 15-20 min video...")
    asyncio.run(_make_mp3(text_to_speak, output))
    return output

if __name__ == "__main__":
    test = "Doston! Aaj hum baat karenge Free Fire ke rise ke baare mein. Kaise 500MB ke is game ne PUBG ko takkar di!"
    make_voiceover(test)













