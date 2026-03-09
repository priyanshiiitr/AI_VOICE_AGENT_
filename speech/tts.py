from elevenlabs.client import ElevenLabs
from config.settings import ELEVENLABS_API_KEY
from typing import Iterator

import sounddevice as sd
import soundfile as sf
import io

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def generate_voice_stream(text: str) -> Iterator[bytes]:
    """
    Stream audio chunks from ElevenLabs in real time
    """

    audio_stream = client.generate(
        text=text,
        voice="21m00Tcm4TlvDq8ikWAM",  # Rachel
        model="eleven_flash_v2_5",
        stream=True
    )

    for chunk in audio_stream:
        if chunk:
            yield chunk


def generate_voice(text: str) -> bytes:
    """
    Generate full audio response (non-streaming)
    """

    audio = client.generate(
        text=text,
        voice="21m00Tcm4TlvDq8ikWAM",
        model="eleven_flash_v2_5"
    )

    audio_bytes = b"".join(audio)

    return audio_bytes


def play_audio(audio_bytes: bytes):
    """
    Play audio bytes through system speakers
    """

    data, samplerate = sf.read(io.BytesIO(audio_bytes))

    sd.play(data, samplerate)
    sd.wait()