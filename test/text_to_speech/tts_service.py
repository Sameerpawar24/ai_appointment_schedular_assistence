
import os
import asyncio
import requests
import tempfile
import soundfile as sf
import sounddevice as sd
from test.core.config import settings

DEEPGRAM_API_KEY = settings.DEEPGRAM_API_KEY
TTS_MODEL = settings.TTS_MODEL


async def speak_text(text: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _speak_blocking, text)


def _speak_blocking(text: str):
    try:
        print("🔊 Generating voice with Deepgram...")

        url = f"https://api.deepgram.com/v1/speak?model={TTS_MODEL}"

        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": text
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            raise Exception(f"{response.status_code} - {response.text}")

        # Save temp WAV (Deepgram returns linear16/wav by default)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(response.content)
            temp_path = f.name

        # Read & play
        data, samplerate = sf.read(temp_path)
        sd.play(data, samplerate)
        sd.wait()

        print(" Playback finished")

    except Exception as e:
        print("TTS Error:", e)





#ELEVAN LAB
# import os
# import asyncio
# from elevenlabs.client import ElevenLabs
# import tempfile
# import soundfile as sf
# import sounddevice as sd

# client = ElevenLabs(api_key="YOUR_ELEVENLABS_API_KEY")

# VOICE_ID = "jUjRbhZWoMK4aDciW36V"  # Rachel voice


# async def speak_text(text: str):
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(None, _speak_blocking, text)


# def _speak_blocking(text: str):
#     try:
#         print("🔊 Generating voice...")

#         audio = client.text_to_speech.convert(
#             voice_id=VOICE_ID,
#             model_id="eleven_multilingual_v2",
#             text=text
#         )

#         audio_bytes = b"".join(audio)

#         # Save temp mp3
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
#             f.write(audio_bytes)
#             temp_path = f.name

#         # Read & play
#         data, samplerate = sf.read(temp_path)
#         sd.play(data, samplerate)
#         sd.wait()

#         print("✅ Playback finished")

#     except Exception as e:
#         print("TTS Error:", e)



# import pyttsx3
# import asyncio

# engine = pyttsx3.init()

# async def speak_text(text):
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(None, _speak_blocking, text)

# def _speak_blocking(text):
#     engine.say(text)
#     engine.runAndWait()
