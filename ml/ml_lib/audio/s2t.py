import whisper
import torch


class WhisperTranscriber:
    def __init__(self, model_size="medium", device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_size)
        if device == "cuda":
            self.model = self.model.to(device)
        self.device = device

    def transcribe_audio(self, audio_path):
        # Transcribe the audio
        result = self.model.transcribe(audio_path)

        return result["text"]
