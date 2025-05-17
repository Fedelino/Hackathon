import requests
import ffmpeg
import tempfile
import os
from io import BytesIO

TOGETHER_API_KEY = "tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8"
voice_id = "helpful woman"


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
    response.raise_for_status()
    return response.content


def create_audio_from_text(text: str, speed: float = 1.2) -> BytesIO:
    raw_audio = generate_audio(text, voice_id)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pcm") as pcm_file:
        pcm_file.write(raw_audio)
        pcm_path = pcm_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
        wav_path = wav_file.name

    try:
        ffmpeg.input(pcm_path, format="f32le", ar=44100, ac=1) \
            .output(wav_path, format="wav", acodec="pcm_s16le", af=f"atempo={speed}") \
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)

        with open(wav_path, "rb") as f:
            audio_bytes = f.read()
        return BytesIO(audio_bytes)

    finally:
        os.remove(pcm_path)
        os.remove(wav_path)
