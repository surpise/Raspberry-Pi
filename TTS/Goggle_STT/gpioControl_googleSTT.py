#!/usr/bin/env python
"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

import argparse
import os
from gpiozero import LED, Button

led = [LED(6), LED(13), LED(19)] 
button = Button(21)
# [START speech_transcribe_sync]
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ko-KR",
    )
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config=config, audio=audio)

    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        str = result.alternatives[0].transcript.split()
    # [END speech_python_migration_sync_response]
    if str[0] == "LED":
        if str[1] == "온":
            for i in range(3):led[i].on()
        elif str[1] == "오프":
            for i in range(3):led[i].off()

# [END speech_transcribe_sync]


# [START speech_transcribe_sync_gcs]
def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    # [START speech_python_migration_config_gcs]
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code="ko-KR",
    )
    # [END speech_python_migration_config_gcs]

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript)) 

# [END speech_transcribe_sync_gcs]


if __name__ == "__main__":
    os.system("mpg123 /home/pi/srcs/tts/guide.mp3")
    while True:
        if button.is_pressed:
            os.system("arecord -f cd -c 1 -d 5 command.wav")
            transcribe_file("command.wav")
