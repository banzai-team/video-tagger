import argparse
import os

from ml_lib.audio.feature_extractor import FeatureExtractor
from ml_lib.video.video_helper import extract_audio_from_video


def process_file(feature_extractor, file_path, output_folder_path, max_duration=None):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    text_file_path = os.path.join(output_folder_path, f"{base_name}.txt")

    if os.path.exists(text_file_path) and os.path.getsize(text_file_path) > 0:
        print(f"Skipping already processed non-empty file: {file_path}")
        return

    print(f"Processing: {file_path}")

    if file_path.endswith((".mp4", ".avi", ".mov")):  # If it's a video file
        audio_path = os.path.join(output_folder_path, f"{base_name}.wav")
        extract_audio_from_video(file_path, audio_path, subclip=(0, max_duration) if max_duration else None)
    else:  # If it's already an audio file
        audio_path = file_path

    print(f"Transcribing: {file_path}")
    text = feature_extractor.extract_features(audio_path)
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(text)
    print(f"Transcribed text saved to: {text_file_path}")

    # Clean up temporary audio file if it was extracted from video
    if file_path.endswith((".mp4", ".avi", ".mov")) and os.path.exists(audio_path):
        os.remove(audio_path)


def extract_all_texts_to_folder(feature_extractor, input_path, output_folder_path, max_duration=None):
    os.makedirs(output_folder_path, exist_ok=True)

    if os.path.isfile(input_path):
        process_file(feature_extractor, input_path, output_folder_path, max_duration)
    elif os.path.isdir(input_path):
        file_paths = [
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if f.endswith((".wav", ".mp4", ".avi", ".mov"))
        ]
        total_files = len(file_paths)

        for idx, file_path in enumerate(file_paths, 1):
            print(f"Processing file {idx} of {total_files}")
            process_file(feature_extractor, file_path, output_folder_path, max_duration)
    else:
        print(f"Error: {input_path} is neither a file nor a directory")


def main(args):
    feature_extractor = FeatureExtractor()
    max_duration = args.max_minutes * 60 if args.max_minutes else None
    extract_all_texts_to_folder(feature_extractor, args.input_path, args.texts_output_path, max_duration)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract text from audio and video files"
    )
    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="Path to the input file or directory containing audio and video files",
    )
    parser.add_argument(
        "--texts_output_path",
        type=str,
        required=True,
        help="Path to the output directory for transcribed texts",
    )
    parser.add_argument(
        "--max_minutes",
        type=int,
        default=None,
        help="Maximum number of minutes to extract from each file (optional)",
    )
    args = parser.parse_args()
    main(args)
