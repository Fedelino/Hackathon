import whisper
from API_call import call_llm
from voice_output_3 import play_audio_from_text
import os

# Load Whisper model
model = whisper.load_model("base")

def talk_to_ai(input_file):
    """
    Transcribes the audio in input_file, sends the text to the LLM,
    and plays back the AI response.
    """
    # Transcribe the audio
    print(f"Transcribing {input_file}...")
    result = model.transcribe(input_file, fp16=False)
    text = result["text"]

    if not text.strip():
        print("No speech detected.")
        return

    print(f"Transcribed: {text}")

    # Call your LLM to get a response
    output_text = call_llm(text)

    # Speak the response
    play_audio_from_text(output_text)
