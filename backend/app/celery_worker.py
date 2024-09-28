import os
from celery import Celery, chain, signature
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
import time
import requests
from app.logger import logger
import yt_dlp
from sqlalchemy.exc import SQLAlchemyError
from app.db.engine import get_db
from app.db.video import Video
from kombu import Queue

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    broker_url=CELERY_BROKER_URL,
    task_queues=[
        Queue("video_upload_queue", routing_key="video_upload_queue"),
        Queue("video_download_queue", routing_key="video_download_queue"),
    ],
    task_routes={
        "app.celery_worker.upload_video": {"queue": "video_upload_queue"},
        "app.celery_worker.download_video": {"queue": "video_download_queue"},
    },
)

celery.conf.update(
    task_track_started=True,
    result_expires=3600,
)


def process_video_tags_for_url(url):
    return chain(
        signature(
            "app.celery_worker.download_video",
            kwargs={"url": url},
            queue="video_upload_queue",
        ),
        signature(
            "app.celery_worker.process_video",
            kwargs={},  # можно здесь добавить какие то доп поля, они будут входными аргами таски
            queue="video_processing_queue",
        ),
    ).delay()


def process_video_tags_for_file(title, description, contents):
    return chain(
        signature(
            "app.celery_worker.upload_video",
            kwargs={"title": title, "description": description, "contents": contents},
            queue="video_upload_queue",
        ),
        signature(
            "app.celery_worker.process_video",
            kwargs={},  # можно здесь добавить какие то доп поля, они будут входными аргами таски
            queue="video_processing_queue",
        ),
    ).delay()


@celery.task(bind=True)
def download_video(self, url, base_path="downloads"):
    logger.debug(f"Running download video job for {url}")
    pls = f"https://rutube.ru/api/play/options/{extract_rutube_id(url)}/?no_404=true&referer=https%3A%2F%2Frutube.ru"

    resp = requests.get(pls)
    if resp.status_code == 200:
        data = resp.json()
        title = data["title"]
        description = data["description"]
        video_id = create_video(
            title, description=description, status="SUBMITTED", url=url
        )
        video_path = base_path + f"/{video_id}/" + "video.mp4"
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": video_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        update_video(video_id, status="DOWNLADED", video_path=video_path)
    else:
        logger.error(f"Video with URL {url} was not found")

    return {"video_id": video_id}


@celery.task(bind=True)
def upload_video(self, title, description, contents, base_path="downloads"):
    logger.debug(f"Uploading video file for {title}")
    video_id = create_video(title, description=description, status="SUBMITTED")
    video_path = base_path + f"/{video_id}/video.mp4"
    os.makedirs(base_path + f"/{video_id}", exist_ok=True)
    with open(video_path, "wb") as f:
        f.write(contents)

    update_video(video_id, status="DOWNLADED", video_path=video_path)

    logger.info("Uploaded video")
    return {"video_id": video_id}


def extract_rutube_id(url):
    if "rutube.ru/video/" in url:
        return url.rstrip("/").split("/")[-1]
    return url


def create_video(title, **kwargs):
    db = next(get_db())
    try:
        video = Video(title=title)
        for key, value in kwargs.items():
            setattr(video, key, value)

        db.add(video)
        db.commit()
        return video.id
    except SQLAlchemyError as e:
        logger.error(f"Error inserting video: {str(e)}")
        db.rollback()  # Откат изменений в случае ошибки
        raise Exception("Unable to persist video")
    finally:
        db.close()  # Закрытие сессии


def update_video(video_id, **kwargs):
    db = next(get_db())
    try:
        q = db.query(Video)
        q = q.filter(Video.id == video_id)
        video = q.one()
        for key, value in kwargs.items():
            setattr(video, key, value)
        db.commit()
        return video
    except SQLAlchemyError as e:
        logger.error(f"Error updating video status: {str(e)}")
        db.rollback()  # Откат изменений в случае ошибки
        raise Exception("Unable to persist video")
    finally:
        db.close()  # Закрытие сессии


if __name__ == "__main__":
    celery.start()
