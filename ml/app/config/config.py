import os

import torch

device = (
    "cuda:0"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)

# Celery configuration
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "filesystem://")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "file:///tmp/celery_results"
)
DATABASE_URL = os.environ.get("DATABASE_URL")

# Ensure the celery directories exist
os.makedirs("/tmp/celery", exist_ok=True)

# env var MODEL_PATH
MODEL_PATH = os.environ.get("LLAMA_MODEL_PATH")
HF_MODEL_NAME = os.environ.get("HF_MODEL_NAME")
FILE_PATH_TRAIN = os.environ.get("FILE_PATH_TRAIN")
FILE_PATH_IAB = os.environ.get("FILE_PATH_IAB")
