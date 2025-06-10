import speech_recognition as sr

def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening for your command...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            text = r.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            print("No command heard.")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""