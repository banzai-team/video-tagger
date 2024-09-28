import argparse


import requests
import json
import cv2
import os
import base64

def extract_file(video_path):

    # Open the video file
    cap = cv2.VideoCapture(video_path)

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
        _, buffer = cv2.imencode('.jpg', frame)
        encoded_frame = base64.b64encode(buffer).decode('utf-8')
        encoded_frames.append(encoded_frame)

    # Prepare the content for the API request
    content = [{"type": "text", "text": "Как думаешь, это фильм, шоу или лекция? "}]
    for encoded_frame in encoded_frames:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_frame}"
            }
        })

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
        },
        json={
            "model": "qwen/qwen-2-vl-72b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
        },
    )

    return response.json()


def main(args):
    print(f"Sending request for video")
    video_path = args.video_path
    text = extract_file(video_path)
    print(f"Extracted text from video: {text}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract text from audio files")
    parser.add_argument(
        "--video_path",
        type=str,
        required=True,
        help="Path to the directory containing audio files",
    )
    args = parser.parse_args()
    main(args)
