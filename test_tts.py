from speech.tts import generate_voice

audio = generate_voice("Hello Priyansh, your voice agent is working")

with open("output.mp3", "wb") as f:
    f.write(audio)