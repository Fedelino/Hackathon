import requests
import ffmpeg
import simpleaudio as sa
import os

TOGETHER_API_KEY = "tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8"


def generate_audio(text: str, voice: str):
    url = "https://api.together.ai/v1/audio/generations"
    headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}"}
    data = {
        "input": text,
        "voice": voice,
        "response_format": "raw",
        "response_encoding": "pcm_f32le",
        "sample_rate": 44100,
        "stream": False,
        "model": "cartesia/sonic",
    }
    response = requests.post(url, headers=headers, json=data)
    return response.content


voice_id = "helpful woman"


def play_audio_from_text(text: str):
    """
    Generates audio from the given text, converts it to WAV, and plays it.

    Assumes `generate_audio` and `voice_id` are defined globally.
    """
    raw_audio = generate_audio(text, voice_id)

    with open("speech.pcm", "wb") as f:
        f.write(raw_audio)

    try:
        ffmpeg.input("speech.pcm", format="f32le", ar=44100, ac=1) \
            .output("speech.wav", format="wav", acodec="pcm_s16le") \
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print("FFmpeg stderr:", e.stderr.decode())
        raise

    wave_obj = sa.WaveObject.from_wave_file("speech.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

    os.remove("speech.wav")
    os.remove("speech.pcm")
