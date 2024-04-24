import speech_recognition as sr
from moviepy.video.io.VideoFileClip import VideoFileClip



def extract_audio_from_video(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()

    
def speech_to_text(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as audio_file:
        audio_data = recognizer.record(audio_file)

        try:
            #text = recognizer.recognize_google(audio_data)  # For Google Web Speech API
            # Alternatively, you can use Sphinx for offline recognition:
            text = recognizer.recognize_sphinx(audio_data)
            return text
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")


