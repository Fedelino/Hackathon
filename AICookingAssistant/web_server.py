from flask import Flask, request, render_template, send_from_directory, send_file
from PIL import Image
from io import BytesIO
import requests
import ffmpeg
import simpleaudio as sa
import os
import tempfile
import subprocess
import os
from flask import send_file, request

from image import classify_food  # reuse image classification
from ask_llm import ask_llm  # LLM that generates recipes
from talk_to_ai import talk_to_ai  # TTS that generates audio from text

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    ingredients = []
    reply = ""
    if request.method == 'POST':
        uploaded_image = request.files.get('image')
        custom_prompt = request.form.get('prompt', '').strip()

        # Use image if provided
        if uploaded_image:
            prediction = classify_food(uploaded_image)
            ingredients = [prediction[0]['label']]

        # Compose prompt
        if ingredients and not custom_prompt:
            full_prompt = f"I have {', '.join(ingredients)}. What is it? From where is it from? And what is the recipe?"
        elif ingredients and custom_prompt:
            full_prompt = f"With {', '.join(ingredients)}, {custom_prompt}"
        else:
            full_prompt = custom_prompt

            if full_prompt:
                raw_reply = ask_llm(full_prompt)
                reply = parse_reply(raw_reply)

    return render_template("index.html", reply=reply, ingredients=ingredients)

    return render_template("index.html", reply=reply, ingredients=ingredients)


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


def parse_reply(reply_text):
    reply = {'title': '', 'ingredients': [], 'steps': []}
    lines = reply_text.strip().splitlines()
    current = None

    for line in lines:
        line = line.strip()

        if not line:
            continue  # skip empty lines

        # Title line (bold markdown style)
        if line.startswith("**") and line.endswith("**") and not reply['title']:
            reply['title'] = line.strip("*").strip()

        # Section headers
        elif "**Ingredients:**" in line:
            current = 'ingredients'
        elif "**Steps:**" in line or "**Instructions:**" in line:
            current = 'steps'

        # Parse items under current section
        elif current == 'ingredients' and line.startswith("-"):
            reply['ingredients'].append(line.lstrip("- ").strip())

        elif current == 'steps' and (line[0].isdigit() and line[1] == '.'):
            reply['steps'].append(line.strip())

    return reply


@app.route("/listen", methods=["POST"])
def listen():
    audio_file = request.files["audio"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as input_tmp:
        audio_file.save(input_tmp.name)
        input_path = input_tmp.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_tmp:
        wav_path = wav_tmp.name

    # Convert input to WAV 16kHz mono
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", wav_path
    ], check=True)

    # Call your talk_to_ai function with the wav_path
    # It should create "reply.wav" or better: return a path or file object
    reply = talk_to_ai(wav_path)

    # Assuming talk_to_ai outputs reply.wav in current dir, send it:
    response = send_file(reply, mimetype="audio/wav")

    # Cleanup temp files
    os.remove(wav_path)
    os.remove(input_path)

    return response


if __name__ == '__main__':
    app.run(debug=True, port=8080)
