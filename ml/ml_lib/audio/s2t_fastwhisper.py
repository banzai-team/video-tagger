import torch
from faster_whisper import WhisperModel


class WhisperTranscriber:
    def __init__(self, model_size="medium", device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = WhisperModel(model_size, device=device, compute_type="int8" if device == "cuda" else "float32", num_workers=4, cpu_threads=4)
        self.device = device

    def transcribe_audio(self, audio_path):
        # Transcribe the audio
        segments, info = self.model.transcribe(audio_path, beam_size=5)

        return "".join([segment.text for segment in segments])

    def transcribe_audio_with_segments(self, audio_path):
        # Transcribe the audio and return a generator of segment texts
        segments, info = self.model.transcribe(audio_path, beam_size=5)

        return (segment for segment in segments)
