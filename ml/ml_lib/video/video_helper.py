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


def extract_audio_from_video(video_path, output_path, subclip=None):
    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    try:
        # Load the video clip
        video = VideoFileClip(video_path)

        # Apply subclip if specified, otherwise use the entire video
        if subclip:
            # Check if video duration is less than the specified subclip end time
            if video.duration < subclip[1]:
                print(f"Warning: Video duration ({video.duration:.2f}s) is less than the specified subclip end time ({subclip[1]}s). Using entire video.")
            else:
                video = video.subclip(*subclip)
        # Extract the audio
        audio = video.audio

        # Write the audio to a file
        audio.write_audiofile(output_path)

        # Close the video to release resources
        video.close()

    except Exception as e:
        print(f"An error occurred while extracting audio: {str(e)}")
