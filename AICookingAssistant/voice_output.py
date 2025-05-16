from gtts import gTTS
from playsound import playsound
import os


def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)  # slow=False = normal pace
    filename = "temp_speech.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)


if __name__ == "__main__":
    speak("Federico is so handsome")
