import websockets
import asyncio

from speech.stt import transcribe_audio
from agent.llm_agent import generate_response
from speech.tts import generate_voice


async def handle_audio(websocket):

    async for audio_chunk in websocket:

        text = await transcribe_audio(audio_chunk)

        print("User:", text)

        reply = generate_response(text)

        print("Agent:", reply)

        voice = generate_voice(reply)

        await websocket.send(voice)


async def main():

    server = await websockets.serve(handle_audio, "0.0.0.0", 8001)

    print("Real-time voice agent running")

    await server.wait_closed()


asyncio.run(main())