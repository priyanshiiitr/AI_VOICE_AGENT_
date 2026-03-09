import asyncio
import sounddevice as sd

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

from config.settings import DEEPGRAM_API_KEY
from agent.llm_agent import generate_response
from speech.tts import generate_voice, play_audio


SAMPLE_RATE = 16000
CHANNELS = 1


async def main():

    loop = asyncio.get_running_loop()

    # Prevent duplicate responses and self-hearing
    last_sentence = ""
    is_speaking = False  # Flag to prevent processing while agent speaks
    
    # Check available microphones
    print("Available audio devices:")
    print(sd.query_devices())
    print()

    # Deepgram setup
    config = DeepgramClientOptions(options={"keepalive": "true"})
    dg_client = DeepgramClient(DEEPGRAM_API_KEY, config)

    dg_connection = dg_client.listen.asyncwebsocket.v("1")

    # =========================
    # Transcript handler
    # =========================
    async def on_message(self, result, **kwargs):

        nonlocal last_sentence, is_speaking

        # Ignore transcripts while agent is speaking (prevent self-hearing)
        if is_speaking:
            return

        sentence = result.channel.alternatives[0].transcript

        if result.is_final and sentence.strip() != "":

            # avoid duplicate responses
            if sentence == last_sentence:
                return

            last_sentence = sentence

            print("\nUser:", sentence)

            # Set speaking flag to pause processing
            is_speaking = True

            try:
                reply = generate_response(sentence)
                print("Agent:", reply)

                audio = generate_voice(reply)
                
                # Use play_audio from tts.py
                play_audio(audio)
                
            finally:
                # Resume processing after speaking
                is_speaking = False

    async def on_close(self, close, **kwargs):
        print("🔌 Deepgram connection closed")

    async def on_error(self, error, **kwargs):
        print("❌ Deepgram error:", error)

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Close, on_close)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    # =========================
    # Deepgram streaming options
    # =========================
    options = LiveOptions(
        model="nova-2",
        language="en-US",
        smart_format=True,
        interim_results=True,
        encoding="linear16",
        channels=CHANNELS,
        sample_rate=SAMPLE_RATE,
        endpointing = 300
    )

    if await dg_connection.start(options) is False:
        print("❌ Deepgram connection failed")
        return

    print("🎤 AI Voice Agent Ready - Speak now!")
    
    # Wait for connection to fully establish
    await asyncio.sleep(0.5)

    # =========================
    # Microphone streaming
    # =========================
    lock = asyncio.Lock()
    audio_chunks_sent = 0
    
    def audio_callback(indata, frames, time_info, status):
        nonlocal audio_chunks_sent

        if status:
            print("⚠️", status)

        audio_bytes = indata.tobytes()
        
        # Only send if we have data
        if len(audio_bytes) > 0:
            audio_chunks_sent += 1
            if audio_chunks_sent % 50 == 0:  # Log every 50 chunks
                print(f"📊 Sent {audio_chunks_sent} audio chunks to Deepgram")
            
            asyncio.run_coroutine_threadsafe(
                send_audio(audio_bytes),
                loop
            )
    
    async def send_audio(audio_bytes):
        """Send audio to Deepgram with error handling"""
        try:
            async with lock:
                await dg_connection.send(audio_bytes)
        except Exception as e:
            pass  # Ignore send errors to prevent spam

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        callback=audio_callback,
        blocksize=8000  # Send audio in consistent chunks
    ):
        print("📡 Microphone active - listening...")
        
        # Send keepalive messages periodically
        async def keepalive():
            while True:
                try:
                    await asyncio.sleep(5)
                    await dg_connection.keep_alive()
                except Exception:
                    break
        
        keepalive_task = asyncio.create_task(keepalive())
        
        try:
            while True:
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
        finally:
            keepalive_task.cancel()
            await dg_connection.finish()


if __name__ == "__main__":
    asyncio.run(main())