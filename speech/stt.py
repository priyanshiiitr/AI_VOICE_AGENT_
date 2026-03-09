from deepgram import DeepgramClient, LiveOptions
from config.settings import DEEPGRAM_API_KEY


dg_client = DeepgramClient(DEEPGRAM_API_KEY)


async def start_live_transcription():

    dg_connection = dg_client.listen.live.v("1")

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        smart_format=True,
        interim_results=True
    )

    await dg_connection.start(options)

    return dg_connection