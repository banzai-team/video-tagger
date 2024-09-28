import os
from ml.ml_lib.video.video_helper import extract_audio_from_video
from pydub import AudioSegment


def cut_audio(fileaudio, max_duration=300):  # 300 seconds = 5 minutes
    sound = AudioSegment.from_wav(fileaudio)
    if len(sound) > max_duration * 1000:  # pydub works in milliseconds
        sound = sound[:max_duration * 1000]
    return sound


def extract_all_texts_from_folder(folder_path, output_folder_path):
    audios_folder = folder_path
    texts_folder = output_folder_path
    os.makedirs(texts_folder, exist_ok=True)

    total_files = len([f for f in os.listdir(audios_folder) if f.endswith('.wav')])
    processed_files = 0

    for file in os.listdir(audios_folder):
        print(f"Found file: {file}")
        print(f"{processed_files} of {total_files}")
        if file.endswith(".wav"):
            text_file_path = os.path.join(texts_folder, f"{file.split('.')[0]}.txt")
            if os.path.exists(text_file_path):
                print(f"Skipping already processed file: {file}")
                processed_files += 1
                continue

            print(f"Processing: {file}")
            audio_path = os.path.join(audios_folder, file)
            
            # Cut audio to 5 minutes max
            cut_audio_segment = cut_audio(audio_path)
            temp_audio_path = os.path.join(audios_folder, f"temp_{file}")
            cut_audio_segment.export(temp_audio_path, format="wav")

            print(f"Transcribing: {file}")
            text = transcriber.transcribe_audio(temp_audio_path)
            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            print(f"Transcribed text saved to: {text_file_path}")
            
            # Remove temporary file
            os.remove(temp_audio_path)
            
            processed_files += 1
            print(f"Progress: {processed_files}/{total_files} files processed")
