import sounddevice as sd
import numpy as np
import whisper
import io
import wave
import requests
from pydub import AudioSegment
from pydub.playback import play

# === SETTINGS ===
TOGETHER_API_KEY = "tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8"
LLM_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
TTS_MODEL = "cartesia/sonic-2"


# === 1. Record audio ===
def record_audio(duration=5, sample_rate=16000):
    print("[🎤] Listening...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    print("[✅] Recording complete.")
    return audio.flatten(), sample_rate


# === 2. Convert to WAV BytesIO (for whisper) ===
def audio_to_wav_bytes(audio, sample_rate):
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    buffer.seek(0)
    return buffer


# === 3. Transcribe using Whisper ===
whisper_model = whisper.load_model("base")


def transcribe_audio(audio_data, sample_rate):
    buffer = audio_to_wav_bytes(audio_data, sample_rate)
    result = whisper_model.transcribe(buffer)
    return result["text"]


# === 4. Ask LLM on Together.ai ===
def ask_llm(user_input):
    system_prompt = "You're a helpful AI cooking assistant. Give short, clear, friendly cooking instructions. Keep it concise."

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.6,
        "max_tokens": 200
    }

    response = requests.post("https://api.together.xyz/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


# === 5. Use Cartesia Sonic-2 to turn text into speech ===
def text_to_speech_together(text, output_path="response.wav"):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": TTS_MODEL,
        "text": text
    }

    response = requests.post("https://api.together.xyz/inference", headers=headers, json=payload)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


# === 6. Play the audio ===
def play_audio(file_path):
    sound = AudioSegment.from_file(file_path)
    play(sound)


# === MAIN LOOP ===
if __name__ == "__main__":
    print("👩‍🍳 AI Cooking Assistant - Speak when ready!")
    while True:
        audio, rate = record_audio(duration=5)
        user_text = transcribe_audio(audio, rate)
        print(f"🗣️ You said: {user_text}")

        if user_text.strip().lower() in ["exit", "quit", "stop"]:
            print("👋 Goodbye!")
            break

        reply = ask_llm(user_text)
        print(f"🤖 AI: {reply}")

        audio_path = text_to_speech_together(reply)
        play_audio(audio_path)
