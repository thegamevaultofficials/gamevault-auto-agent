import os
import asyncio
import edge_tts

def make_voiceover(text, output_path="voice.mp3"):
    text = text.strip().replace("\n", " ")[:1500]
    if not text:
        text = "Hello gamers, welcome to Game Vault."
    
    # Clean old file
    if os.path.exists(output_path):
        os.remove(output_path)
    
    async def _edge():
        comm = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
        await comm.save(output_path)
    
    # Try Edge-TTS 2 times
    for i in range(2):
        try:
            asyncio.run(_edge())
            if os.path.exists(output_path) and os.path.getsize(output_path) > 5000:
                print(f"Voice done with Edge-TTS, size: {os.path.getsize(output_path)}")
                return
        except Exception as e:
            print(f"Edge attempt {i+1} failed: {e}")
    
    # FALLBACK to gTTS if Edge fails
    print("Trying gTTS fallback...")
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save(output_path)
        print(f"Voice done with gTTS fallback")
        return
    except Exception as e:
        print(f"gTTS also failed: {e}")
        raise Exception("Both TTS failed")
