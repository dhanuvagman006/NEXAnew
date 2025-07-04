import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
from pydub.playback import play
import io
from gtts import gTTS
import pyttsx3

api_key = "FztRh0MY8wTsyNcUKcBkXq7phL0TQlL08MBo3XMmuysCZfgy8RpIJQQJ99BFACYeBjFXJ3w3AAAYACOGN1GL"  # Consider moving this to an environment variable
region = "eastus"
engine = pyttsx3.init(driverName='espeak')  # For Linux
engine.setProperty('rate', 150)     # Speed (default ~200)
engine.setProperty('volume', 1.0)   # Volume (0.0 to 1.0)

def play_audio(audio_data, format='wave'):
    audio_data_io = io.BytesIO(audio_data)
    audio_segment = AudioSegment.from_file(audio_data_io, format=format)
    play(audio_segment)


speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name = 'en-AU-CarlyNeural'

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def def_play(text):
    engine.say(text)
    engine.runAndWait()

def speech_play(text):
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized and played for: '{text}'")
    elif result.reason == speechsdk.ResultReason.Canceled:
        def_play(text)
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
    else:
        print(f"Speech synthesis failed: {result.reason}")
    return "Done,synthesized and played"


def voice_to_text():
    """Captures audio from the microphone and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        print(e)
        return None
        # return "Sorry,can you repeat again"
if __name__ == '__main__':
    print(speech_play(voice_to_text()))