import whisper
from API_call import call_llm
from generate_voice_output import create_audio_from_text

# Load Whisper model
model = whisper.load_model("base")


def talk_to_ai(input_file):
    """
    Transcribes the audio in input_file, sends the text to the LLM,
    generates the AI response audio, and returns the path to the audio file.
    """
    print(f"Transcribing {input_file}...")
    result = model.transcribe(input_file, fp16=False)
    text = result["text"]

    if not text.strip():
        print("No speech detected.")
        return None

    print(f"Transcribed: {text}")

    output_text = call_llm(text)

    # Generate the audio file but don't play it, just return the path
    reply_audio_path = create_audio_from_text(output_text)

    return reply_audio_path
