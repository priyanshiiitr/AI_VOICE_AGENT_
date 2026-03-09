import asyncio
import sounddevice as sd
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)
from config.settings import DEEPGRAM_API_KEY

SAMPLE_RATE = 16000
CHANNELS = 1


async def main():
    """Real-time speech-to-text streaming with Deepgram"""

    # Get current event loop
    loop = asyncio.get_running_loop()

    # Configure Deepgram client
    config = DeepgramClientOptions(options={"keepalive": "true"})
    dg_client = DeepgramClient(DEEPGRAM_API_KEY, config)

    # Create WebSocket connection
    dg_connection = dg_client.listen.asyncwebsocket.v("1")

    # ===============================
    # Event Handlers
    # ===============================

    async def on_message(self, result, **kwargs):

        sentence = result.channel.alternatives[0].transcript

        if sentence:

            if result.is_final:
                print(f"✅ Final: {sentence}")
            else:
                print(f"⏳ Interim: {sentence}")

    async def on_error(self, error, **kwargs):
        print(f"❌ Error: {error}")

    async def on_close(self, close, **kwargs):
        print("🔌 Connection closed")

    # Register event handlers
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)
    dg_connection.on(LiveTranscriptionEvents.Close, on_close)

    # ===============================
    # Deepgram Options
    # ===============================

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        smart_format=True,
        interim_results=True,
        encoding="linear16",
        channels=CHANNELS,
        sample_rate=SAMPLE_RATE,
    )

    # Start connection
    if await dg_connection.start(options) is False:
        print("❌ Failed to connect to Deepgram")
        return

    print("🎤 Start speaking... (Press Ctrl+C to stop)")

    # ===============================
    # Audio Callback
    # ===============================

    def audio_callback(indata, frames, time_info, status):

        if status:
            print(f"⚠️ Audio status: {status}")

        audio_bytes = indata.tobytes()

        # Send audio safely to asyncio loop
        asyncio.run_coroutine_threadsafe(
            dg_connection.send(audio_bytes),
            loop
        )

    # Start microphone stream
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        callback=audio_callback,
    ):

        try:
            while True:
                await asyncio.sleep(0.1)

        except KeyboardInterrupt:
            print("\n🛑 Stopping...")

        finally:
            await dg_connection.finish()


if __name__ == "__main__":
    asyncio.run(main())