import asyncio

# This example uses the sounddevice library to get an audio stream from the
# microphone. It's not a dependency of the project but can be installed with
# `pip install sounddevice`.
import sounddevice


from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
import os
from gpiozero import LED
from time import sleep

"""
Here's an example of a custom event handler you can extend to
process the returned transcription results as needed. This
handler will simply print the text out to your interpreter.
"""
led = [LED(6), LED(13), LED(19)] 
num = ['영', '일', '이', '삼', '사', '오', '육', '칠']
sign = ['플러스', '마이너스']
class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        # This handler can be implemented to handle transcriptions as needed.
        # Here's an example to get started.
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                str = alt.transcript.split()
                print(str)
            if len(str) > 1:

                if str[0] == 'First': select = 0
                elif str[0] == 'Second': select = 1
                elif str[0] == 'Third': select = 2
                elif str[0] == 'Domino' :
                    i = 0
                    os.system("mpg321 /home/pi/srcs/tts/domino.mp3")
                    for j in range(10):
                        sleep(0.5)
                        i = (i + 1) % 3
                        led[i].on()
                        sleep(0.5)
                    led[i].off()

                if str[1] == 'on' and led[select].value == 0: 
                    led[select].on()
                    os.system(f'mpg321 /home/pi/srcs/tts/LED{select+1}_on.mp3')
                elif str[1] == 'off' and led[select].value == 1: 
                    led[select].off()
                    os.system(f'mpg321 /home/pi/srcs/tts/LED{select+1}_off.mp3')
            

async def mic_stream():
    # This function wraps the raw input stream from the microphone forwarding
    # the blocks to an asyncio.Queue.
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    # Be sure to use the correct parameters for the audio stream that matches
    # the audio formats described for the source language you'll be using:
    # https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=44100,
        callback=callback,
        blocksize=1024 * 2,
        dtype="int16",
    )
    # Initiate the audio stream and asynchronously yield the audio chunks
    # as they become available.
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    # This connects the raw audio chunks generator coming from the microphone
    # and passes them along to the transcription stream.
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe():
    # Setup up our client with our chosen AWS region
    client = TranscribeStreamingClient(region="us-east-1")

    # Start transcription to generate our async stream
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=44100,
        media_encoding="pcm",
    )

    # Instantiate our handler and start processing events
    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(stream), handler.handle_events())

os.system("mpg123 /home/pi/srcs/tts/rule.mp3")
loop = asyncio.get_event_loop()
loop.run_until_complete(basic_transcribe())
loop.close()
