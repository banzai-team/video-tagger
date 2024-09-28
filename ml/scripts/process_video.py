import argparse
import requests
import json
import cv2
import os
import base64
from pathlib import Path

OPENAI_KEY = os.environ.get("OPENAI_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai")
MODEL = "qwen/qwen-2-vl-72b-instruct"

prompt = """
Я отправляю тебе 10 картинок, которые являются кадрами из видео.
Ваша задача — описать видео, которое соответствует этим кадрам.
Суммируй информацию из всех кадров в одном предложении.

Пример1: Это фильм про путешествия.
Пример2: Это шоу про еду.
Пример3: Это геймплей игры.
"""


def extract_file(video_path):
    # Open the video file
    cap = cv2.VideoCapture(str(video_path))

    # Get total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the step size to get 10 equally distributed frames
    step = total_frames // 10

    frames = []
    for i in range(10):
        # Set the frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)

        # Read the frame
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    # Release the video capture object
    cap.release()

    # Encode frames to base64
    encoded_frames = []
    for i, frame in enumerate(frames):
        _, buffer = cv2.imencode(".jpg", frame)
        encoded_frame = base64.b64encode(buffer).decode("utf-8")
        encoded_frames.append(encoded_frame)

    # Prepare the content for the API request
    content = [{"type": "text", "text": prompt}]
    for encoded_frame in encoded_frames:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_frame}"},
            }
        )

    response = requests.post(
        url=f"{OPENAI_BASE_URL}/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ.get('OPENAI_KEY')}",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": content}],
        },
    )

    if response.status_code >= 300:
        raise Exception(
            f"API request failed with status code {response.status_code}: {response.text}"
        )
    try:
        return {"content": response.json()["choices"][0]["message"]["content"]}
    except (KeyError, IndexError, json.JSONDecodeError):
        raise Exception(f"Error: Unable to parse JSON response. Response: {response.text}")


def process_video(video_path, output_dir):
    output_path = output_dir / video_path.with_suffix(".json").name
    if output_path.exists():
        print(f"Skipping {video_path}: Output file already exists at {output_path}")
        return

    print(f"Processing video: {video_path}")
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            result = extract_file(video_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Results saved to: {output_path}")
            break
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"Error occurred: {str(e)}. Retrying... (Attempt {retry_count}/{max_retries})")
            else:
                print(f"Failed to process {video_path} after {max_retries} attempts. Error: {str(e)}")


def main(args):
    input_path = Path(args.input)
    output_dir = Path(args.output_dir) if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    if input_path.is_file():
        process_video(input_path, output_dir)
    elif input_path.is_dir():
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import multiprocessing

        def process_video_wrapper(args):
            video_file, output_dir = args
            process_video(video_file, output_dir)

        max_workers = min(multiprocessing.cpu_count(), 10)  # Use up to 10 workers or CPU count, whichever is smaller
        video_files = list(input_path.glob("*.mp4"))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_video_wrapper, (video_file, output_dir)) for video_file in video_files]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"An error occurred while processing a video: {str(e)}")
    else:
        print(f"Error: {input_path} is neither a file nor a directory")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process video files and extract information"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to a video file or directory containing video files",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Path to the output directory (default: same directory as the video)",
    )
    args = parser.parse_args()
    main(args)
