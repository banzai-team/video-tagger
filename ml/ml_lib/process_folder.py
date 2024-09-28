from .video.video_helper import extract_audio_from_video
from .audio.s2t import WhisperTranscriber


transcriber = WhisperTranscriber()


def extract_text_from_video(video_path):
    audio_path = extract_audio_from_video(video_path)
    text = transcriber.transcribe_audio(audio_path)
    
    return text
