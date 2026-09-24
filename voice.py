import asyncio
import edge_tts

VOICE = "hi-IN-MadhurNeural"
RATE = "+5%"
PITCH = "+0Hz"

async def _make_mp3(text, output="voiceover.mp3"):
    communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(output)
    print(f"Saved: {output}")
    return output

def make_voiceover(full_script, output="voiceover.mp3"):
    text_to_speak = full_script[:15000]
    asyncio.run(_make_mp3(text_to_speak, output))
    return output
