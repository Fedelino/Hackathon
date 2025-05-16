import requests
from pydub import AudioSegment
from pydub.playback import play

TOGETHER_API_KEY = "tgp_v1_K551Xt2XcS1IEuA3jLXw3PGc7kvh5NZrcKjbmxX3va8"
TTS_MODEL = "cartesia/sonic-2"

def speak(text):
    print(f"[🗣️] Speaking: {text}")

    url = "https://api.together.ai/inference"  # ✅ updated endpoint

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TTS_MODEL,
        "input": {
            "text": text
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("❌ Error:", response.status_code, response.text)
        return

    # Save and play the audio file
    with open("output.wav", "wb") as f:
        f.write(response.content)

    audio = AudioSegment.from_file("output.wav")
    play(audio)

if __name__ == "__main__":
    while True:
        user_input = input("Say something (or type 'exit'): ")
        if user_input.strip().lower() == "exit":
            break
        speak(user_input)
