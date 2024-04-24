from stt import *
from summ import *
from vtt import *
import  os

def main():
    video_file_path = "C:/Users/anirb/Audio summarizer/my models/Learn How to Solve a Rubiks Cube in 10 Minutes (Beginner Tutorial).mp4"
    audio_output_path = "C:/Users/anirb/Audio summarizer/my models/out_audio.wav"
    text_output_path = "C:/Users/anirb/Audio summarizer/my models/transcribed_text.txt"
    summary_output_path = "C:/Users/anirb/Audio summarizer/my models/summary.txt"
    
    if not os.path.exists(video_file_path):
        print(f"Error: Video file not found at {video_file_path}")
        return

    try:
        extract_audio_from_video(video_file_path, audio_output_path)
        transcribed_text = speech_to_text(audio_output_path)

        if transcribed_text:
            # Write transcribed text to a text file
            with open(text_output_path, "w") as text_file:
                text_file.write(transcribed_text)

            # Generate summary from transcribed text
            summary = generate_summary_from_text(text_output_path, video_file_path)

            # Write summary to a text file
            with open(summary_output_path, "w") as summary_file:
                summary_file.write(summary)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
