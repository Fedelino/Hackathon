from flask import Flask, request, render_template, send_from_directory
from PIL import Image
from io import BytesIO
import requests
import ffmpeg
import simpleaudio as sa
import os

from image import classify_food  # reuse image classification
from API_call import call_llm  # reuse LLM prompt call
from voice_output_3 import generate_audio  # reuse TTS generation

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
            image = Image.open(uploaded_image)
            prediction = classify_food(image)
            ingredients = [item['label'] for item in prediction[:3]]

        # Compose prompt
        if ingredients and not custom_prompt:
            full_prompt = f"I have {', '.join(ingredients)}. What can I cook with them?"
        elif ingredients and custom_prompt:
            full_prompt = f"With {', '.join(ingredients)}, {custom_prompt}"
        else:
            full_prompt = custom_prompt

        # Call LLM and TTS
        if full_prompt:
            reply = call_llm(full_prompt)
            generate_audio(reply)  # writes to static/speech.wav

    return render_template("index.html", ingredients=ingredients, reply=reply)


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
