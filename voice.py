import edge_tts
import asyncio

async def _make(text, file="gamevault_final.mp3"):
    communicate = edge_tts.Communicate(
        text=text,
        voice="hi-IN-MadhurNeural",
        rate="+15%",
        pitch="+2Hz"
    )
    await communicate.save(file)

def make_voiceover(text):
    text = text.replace("500MB", "पाँच सौ एमबी")
    text = text.replace("MB", "एमबी")
    text = text.replace("GB", "जीबी")
    text = text.replace("Free Fire", "फ्री फायर")
    asyncio.run(_make(text))
    print("Voice done")
