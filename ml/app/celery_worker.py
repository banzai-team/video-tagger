import os
from celery import Celery, chain
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
import time
from kombu import Queue
from app.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from app.db.engine import get_db
from app.db.video import Video
from ml_lib.audio.s2t import WhisperTranscriber
from ml_lib.video.video_helper import extract_audio_from_video


celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    broker_url=CELERY_BROKER_URL,
    task_queues=[
        Queue("video_processing_queue", routing_key="video_processing_queue"),
        Queue("audio_extraction_queue", routing_key="audio_extraction_queue"),
        Queue("s2t", routing_key="s2t"),
        Queue("process_video_text", routing_key="process_video_text"),
    ],
    task_routes={
        "app.celery_worker.process_video": {"queue": "video_processing_queue"},
        "app.celery_worker.extract_audio": {"queue": "audio_extraction_queue"},
        "app.celery_worker.s2t": {"queue": "s2t"},
        "app.celery_worker.process_video_text": {"queue": "process_video_text"},
    },
)

celery.conf.update(
    task_track_started=True,
    result_expires=3600,
)


@celery.task(bind=True)
def process_video(self, input, **kwargs):
    # Создание цепочки задач
    logger.debug(
        f"Processing video with params: {str(input)}, additional params: {str(kwargs)}"
    )
    task_chain = chain(
        extract_audio.s(input),
        s2t.s(),
        process_video_text.s(),
    )

    # Запуск цепочки задач
    result = task_chain.apply_async()

    return result


@celery.task(bind=True)
def extract_audio(self, input, **kwargs):
    video_id = input["video_id"]
    video = get_video_by_id(video_id=video_id)
    audio_output_path = f"./downloads/{video_id}/audio.wav"
    extract_audio_from_video(video_path=video.video_path, output_path=audio_output_path)
    update_video(
        video_id=video_id, status="AUDIO_EXTRACTED", audio_path=audio_output_path
    )
    return {"video_id": video_id, "audio_path": audio_output_path}


@celery.task(bind=True)
def s2t(self, input, **kwargs):
    video_id = input["video_id"]
    audio_path = input["audio_path"]
    s2tModel = WhisperTranscriber()

    text = s2tModel.transcribe_audio(audio_path)
    update_video(video_id=video_id, status="TEXT_EXTRACTED", text=text)

    return {"video_id": video_id, "text": text}


@celery.task(bind=True)
def process_video_text(self, input, **kwargs):
    video_id = input["video_id"]
    text = input["text"]
    logger.info(f"Extracted video text: {text}")

    update_video(video_id=video_id, status="TEXT_PROCESSED", tags='["kids", "cartoon"]')

    return {"status": "OK"}


def get_video_by_id(video_id):
    db = next(get_db())
    q = db.query(Video)
    q = q.filter(Video.id == video_id)
    return q.one()


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
