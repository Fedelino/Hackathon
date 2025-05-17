import requests
import ffmpeg
from io import BytesIO

TOGETHER_API_KEY = "tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8"
voice_id = "helpful woman"


def generate_audio(text: str, voice: str) -> bytes:
    url = "https://api.together.ai/v1/audio/generations"
    headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}"}
    data = {
        "input": text,
        "voice": voice,
        "response_format": "raw",
        "response_encoding": "pcm_f32le",
        "sample_rate": 44100,
        "stream": False,
        "model": "cartesia/sonic-2",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.content


def create_audio_from_text(text: str, speed: float = 1.0) -> BytesIO:
    raw_audio = generate_audio(text, voice_id)

    in_buf = BytesIO(raw_audio)
    out_buf = BytesIO()

    process = (
        ffmpeg
        .input("pipe:0", format="f32le", ar=44100, ac=1)
        .output("pipe:1", format="wav", acodec="pcm_s16le", af=f"atempo={speed}")
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    out, err = process.communicate(input=in_buf.read())
    out_buf.write(out)
    out_buf.seek(0)
    return out_buf
