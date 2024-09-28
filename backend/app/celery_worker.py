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

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    broker_url=CELERY_BROKER_URL,
)

celery.conf.update(
    task_track_started=True,
    result_expires=3600,
)


def process_video_tags_for_url(url):
    return chain(download_video.s(url)).delay()


def process_video_tags_for_file(title, file):
    return chain(upload_video.s(title, file)).delay()


@celery.task(bind=True)
def download_video(self, url, base_path="./downloads"):
    logger.debug(f"Running download video job for {url}")
    pls = f"https://rutube.ru/api/play/options/{extract_rutube_id(url)}/?no_404=true&referer=https%3A%2F%2Frutube.ru"
    resp = requests.get(pls)

    if resp.status_code == 200:
        data = resp.json()
        logger.info(data)
        rutube_id = data["id"]
        title = data["title"]
        file_path = base_path + f"/{rutube_id}/" + "video.mp4"
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": file_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        db = next(get_db())
        try:
            db.add(
                Video(title=title, file_path=file_path, status="DOWNLOADED", url=url)
            )
            db.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error inserting video: {str(e)}")
            db.rollback()  # Откат изменений в случае ошибки
        finally:
            db.close()  # Закрытие сессии
    else:
        logger.error(f"Video with URL {url} was not found")


@celery.task(bind=True)
def upload_video(self, title, contents, base_path="./downloads"):
    logger.debug(f"Uploading video file for {title}")
    file_id = uuid.uuid4()
    file_path = base_path + f"/{file_id}/video.mp4"
    os.makedirs(base_path + f"/{file_id}", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(contents)
    db = next(get_db())
    try:
        db.add(Video(title=title, file_path=file_path, status="DOWNLOADED"))
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error inserting video: {str(e)}")
        db.rollback()  # Откат изменений в случае ошибки
    finally:
        db.close()  # Закрытие сессии


def extract_rutube_id(url):
    if "rutube.ru/video/" in url:
        return url.rstrip("/").split("/")[-1]
    return url


@celery.task(bind=True)
def process_video(self, video_id):
    # Simulating video processing
    for i in range(100):
        self.update_state(state="PROGRESS", meta={"progress": i})
        time.sleep(0.1)
    return {"status": "completed"}


if __name__ == "__main__":
    celery.start()
