import asyncio
from speech.stt import transcribe_audio

with open("Recording.m4a", "rb") as f:
    audio = f.read()

text = asyncio.run(transcribe_audio(audio))

print("Transcription:", text)