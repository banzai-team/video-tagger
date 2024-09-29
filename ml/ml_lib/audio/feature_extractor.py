from .s2t import WhisperTranscriber
# from .s2t_fastwhisper import WhisperTranscriber


class FeatureExtractor:
    def __init__(self):
        self.transcriber = WhisperTranscriber()

    def extract_features(self, audio_path, min_duration=1):
        # from pydub import AudioSegment

        # # Load the audio file
        # audio = AudioSegment.from_file(audio_path)

        # # Extract the first n minutes
        # n_minutes = min_duration * 60 * 1000  # n minutes in milliseconds
        # audio_excerpt = audio[:n_minutes]

        # import os
        # import tempfile

        # # Create a temporary file in the system's temporary directory
        # with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        #     temp_audio_path = temp_file.name

        # # Export the excerpt to the temporary file
        # audio_excerpt.export(temp_audio_path, format="wav")

        # # Transcribe the excerpt
        # text = self.transcriber.transcribe_audio(temp_audio_path)

        # # Clean up the temporary file
        # os.remove(temp_audio_path)

        text = self.transcriber.transcribe_audio(audio_path)
        return text
