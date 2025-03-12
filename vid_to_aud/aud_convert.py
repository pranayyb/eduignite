from pydub import AudioSegment
import os

def video_to_audio(video_path, output_audio_path, audio_format="mp3"):
    try:
        audio = AudioSegment.from_file(video_path)
        audio.export(output_audio_path, format=audio_format)
        print(f"Conversion successful! Audio saved at: {output_audio_path}")
    except Exception as e:
        print(f"Error: {e}")


video_path = "lec_6.mp4"  
output_audio_path = "output_audio.mp3"  

# video_to_audio(video_path, output_audio_path)
