
import os
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import requests
from test.core.config import settings

DEEPGRAM_API_KEY = settings.DEEPGRAM_API_KEY
DEEPGRAM_URL = settings.DEEPGRAM_URL


async def listen_once():
    try:
        print("\n🎙️ Listening...")

        duration = 5
        sample_rate = 16000

        # Record from microphone
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
        )
        sd.wait()

        # Save temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            write(f.name, sample_rate, recording)
            temp_filename = f.name

        with open(temp_filename, "rb") as audio:
            audio_bytes = audio.read()

        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav",
        }

        params = {
            "model": "nova-2",
            "smart_format": "true", 
        }

        # Call Deepgram REST API
        resp = requests.post(DEEPGRAM_URL, headers=headers, params=params, data=audio_bytes)

        if resp.status_code != 200:
            print("Deepgram Error:", resp.text)
            return None

        data = resp.json()

        transcript = (
            data["results"]["channels"][0]["alternatives"][0]["transcript"]
            if "results" in data
            else None
        )

        return transcript.strip() if transcript else None

    except Exception as e:
        print("Deepgram STT Error:", e)
        return None






# import speech_recognition as sr
# import asyncio

# recognizer = sr.Recognizer()

# # Increase energy threshold stability
# recognizer.energy_threshold = 300
# recognizer.pause_threshold = 0.8

# mic = sr.Microphone()

# async def listen_once():
#     loop = asyncio.get_event_loop()

#     try:
#         with mic as source:
#             print("\n🎙️ Listening...")
#             recognizer.adjust_for_ambient_noise(source, duration=0.5)

#             audio = recognizer.listen(
#                 source,
#                 timeout=5,              # wait max 5 sec for speech
#                 phrase_time_limit=10    # max sentence length
#             )

#         text = await loop.run_in_executor(
#             None,
#             lambda: recognizer.recognize_google(audio)
#         )

#         return text.strip()

#     except sr.WaitTimeoutError:
#         # No speech detected
#         return None

#     except sr.UnknownValueError:
#         print("⚠ Could not understand audio")
#         return None

#     except Exception as e:
#         print("STT Error:", e)
#         return None
