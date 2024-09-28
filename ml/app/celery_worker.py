import os
from celery import Celery, chain
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
import time
import requests
from app.logger import logger
import yt_dlp
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import uuid
from app.db.engine import get_db
from app.db.video import Status, Video
from kombu import Queue

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    broker_url=CELERY_BROKER_URL,
    task_queues=[
        Queue("video_processing_queue", routing_key="video_processing_queue"),
    ],
    task_routes={
        "app.celery_worker.process_video": {"queue": "video_processing_queue"},
    },
)

celery.conf.update(
    task_track_started=True,
    result_expires=3600,
)


@celery.task(bind=True)
def process_video(self, video_id, **kwargs):
    # Simulating video processing
    logger.info(f"Processing! {str(kwargs), {str(video_id)}}")
    for i in range(100):
        self.update_state(state="PROGRESS", meta={"progress": i})
        time.sleep(0.1)
    return {"status": "completed"}


if __name__ == "__main__":
    celery.start()
