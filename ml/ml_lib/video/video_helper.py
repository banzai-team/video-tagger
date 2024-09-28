import yt_dlp
import os
from moviepy.editor import VideoFileClip


def download_video_from_url(url, output_path="./data/downloaded_video.mp4"):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_path,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path


def extract_audio_from_video(video_path, output_path):
    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    try:
        # Load the video clip
        video = VideoFileClip(video_path)

        # Extract the audio
        audio = video.audio

        # Write the audio to a file
        audio.write_audiofile(output_path)

        # Close the video to release resources
        video.close()

    except Exception as e:
        print(f"An error occurred while extracting audio: {str(e)}")
