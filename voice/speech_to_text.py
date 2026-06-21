import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_and_convert(self, lang='tr-TR'):
        with sr.Microphone() as source:
            print("Dinliyor...")
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio, language=lang)
            print(f"Söylenen: {text}")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None