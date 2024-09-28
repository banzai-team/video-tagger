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


def process_video(video_path):
    print(f"Processing video: {video_path}")
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            result = extract_file(video_path)
            print(f"Video processed successfully: {video_path}")
            return result['content']
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"Error occurred: {str(e)}. Retrying... (Attempt {retry_count}/{max_retries})")
            else:
                print(f"Failed to process {video_path} after {max_retries} attempts. Error: {str(e)}")
                return None