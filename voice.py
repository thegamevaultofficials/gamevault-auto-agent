import asyncio
import edge_tts

def make_voiceover(text, output_path="voice.mp3"):
    # Clean text - remove too long
    text = text.strip()[:1000]
    
    async def _speak():
        # hi-IN-MadhurNeural = Best Hinglish male voice
        communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
        await communicate.save(output_path)
    
    try:
        asyncio.run(_speak())
        print(f"Voice done: {output_path}")
    except Exception as e:
        print(f"Voice error: {e}")
        # fallback try again
        asyncio.run(_speak())

# For compatibility with your old main.py that calls with 1 arg
# This also works: make_voiceover(script, "voice.mp3")
# And this also works: make_voiceover(script)
