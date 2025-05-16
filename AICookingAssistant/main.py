import numpy as np
import sounddevice as sd
import whisper
import queue
from API_call import call_llm
from vice_output_3 import play_audio_from_text

model = whisper.load_model("base")

# Audio settings
samplerate = 16000
channels = 1
block_duration = 0.5  # seconds of audio per block

q = queue.Queue()


def audio_callback(indata, frames, time_, status):
    if status:
        print(status)
    q.put(indata.copy())


def is_silence(data, threshold=0.01):
    """Simple silence detection by RMS amplitude."""
    return np.sqrt(np.mean(data ** 2)) < threshold


def main():
    print("Starting continuous speech recognition... (press Ctrl+C to stop)")

    audio_buffer = []

    with sd.InputStream(samplerate=samplerate, channels=channels, callback=audio_callback):
        while True:
            try:
                # Collect 1 second audio blocks
                audio_chunk = q.get()
                audio_buffer.append(audio_chunk)

                # Flatten buffer to 1D numpy array
                audio_data = np.concatenate(audio_buffer, axis=0).flatten()

                # Check for silence at the end of buffer
                if is_silence(audio_data[-samplerate // 2:]):  # last 0.5 sec silence
                    if len(audio_data) > samplerate // 2:  # only transcribe if >0.5 sec audio
                        # Normalize audio to float32 (-1 to 1)
                        audio_norm = audio_data.astype(
                            np.float32) / 32768.0 if audio_data.dtype == np.int16 else audio_data.astype(np.float32)

                        # Run Whisper transcription
                        result = model.transcribe(audio_norm, fp16=False)
                        text = result["text"]

                        if text:
                            print(f"Transcribed: {text}")
                            output_text = call_llm(text)
                            play_audio_from_text(output_text)

                    # Clear buffer after transcribing silence
                    audio_buffer = []

            except KeyboardInterrupt:
                print("\nStopped by user")
                break


if __name__ == "__main__":
    main()
