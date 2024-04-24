import speech_recognition as sr

def real_time_speech_to_text(timeout=30):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")

        while True:
            try:
                audio_data = recognizer.listen(source, timeout=timeout)
                text = recognizer.recognize_google(audio_data)
                print("Text from speech:")
                print(text)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")

            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

            except sr.WaitTimeoutError:
                print(f"No speech detected for {timeout} seconds. Restarting listening...")
