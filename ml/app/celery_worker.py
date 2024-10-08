import os
from celery import Celery, chain
from app.config import (
    MODEL_NAME,
    HF_MODEL_NAME,
    OPENROUTER_MODEL_NAME,
    FILE_PATH_PREDICT,
    FILE_PATH_IAB,
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    ENABLE_S2T,
    ENABLE_FRAMES_DESCR,
)
import time
from kombu import Queue
from app.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from app.db.engine import get_db
from app.db.video import Video
from ml_lib.audio.feature_extractor import FeatureExtractor
from ml_lib.model_registry import load_model_hf, load_model_openrounter
from ml_lib.utils import create_nested_structure, load_data
from scripts.pipelines.llm_hierarcial import VideoFeatures, predict_video
from ml_lib.video.video_helper import extract_audio_from_video
from ml_lib.video_llm.process_frames import process_video as analyze_frames


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
print_model_info = f"""
Initializing model with
    FILE_PATH_TRAIN: {FILE_PATH_PREDICT}
    FILE_PATH_IAB: {FILE_PATH_IAB}
    MODEL_NAME: {MODEL_NAME}
    HF_MODEL_NAME: {HF_MODEL_NAME}
    OPENROUTER_MODEL_NAME: {OPENROUTER_MODEL_NAME}
"""
logger.info(print_model_info)

data, taxonomy, video_desc_dict, s2t_dict = load_data(
    file_path_train=FILE_PATH_PREDICT, file_path_iab=FILE_PATH_IAB
)
nested_taxonomy = create_nested_structure(taxonomy)  # type: dict[str, dict[str, list]]

if MODEL_NAME == "hf":
    lm = load_model_hf(HF_MODEL_NAME)
elif MODEL_NAME == "openrouter":
    lm = load_model_openrounter(OPENROUTER_MODEL_NAME)
else:
    raise NotImplementedError(f"{MODEL_NAME}")
data, taxonomy, video_desc_dict, s2t_dict = load_data(
    file_path_train=FILE_PATH_PREDICT, file_path_iab=FILE_PATH_IAB
)
nested_taxonomy = create_nested_structure(taxonomy)  # type: dict[str, dict[str, list]]

logger.info("""Model initialized""")

s2tModel = FeatureExtractor()


@celery.task(bind=True)
def process_video(self, input, **kwargs):
    # Создание цепочки задач
    logger.debug(
        f"Processing video with params: {str(input)}, additional params: {str(kwargs)}"
    )
    if ENABLE_S2T:
        if ENABLE_FRAMES_DESCR:
            task_chain = chain(
                extract_audio.s(input),
                s2t.s(),
                text_from_frames.s(),
                process_video_text.s(),
            )
        else:
            task_chain = chain(
                extract_audio.s(input),
                s2t.s(),
                process_video_text.s(),
            )
    else:
        if ENABLE_FRAMES_DESCR:
            task_chain = chain(
                extract_audio.s(input), text_from_frames.s(), process_video_text.s()
            )
        else:
            task_chain = chain(
                extract_audio.s(input),
                process_video_text.s(),
            )
    # task_chain = chain(extract_audio.s(input) | s2t.s() | process_video_text.s())

    # Запуск цепочки задач
    result = task_chain.apply_async()

    return result


@celery.task(bind=True)
def extract_audio(self, input, **kwargs):
    video_id = input["video_id"]
    video = get_video_by_id(video_id=video_id)
    audio_output_path = f"./downloads/{video_id}/audio.wav"
    logger.debug(f"Extracting audio from video: {video_id}")
    extract_audio_from_video(video_path=video.video_path, output_path=audio_output_path)
    update_video(
        video_id=video_id, status="AUDIO_EXTRACTED", audio_path=audio_output_path
    )
    logger.debug(f"Extracted audio from video {video_id} into {audio_output_path}")
    return {"video_id": video_id, "audio_path": audio_output_path}


@celery.task(bind=True)
def s2t(self, input, **kwargs):
    video_id = input["video_id"]
    video = get_video_by_id(video_id=video_id)
    audio_path = video.audio_path
    logger.debug(f"Executing s2tfor video: {video_id}")

    text = s2tModel.extract_features(audio_path)
    update_video(video_id=video_id, status="TEXT_EXTRACTED", text=text)

    logger.debug(f"s2t completed for video: {video_id}")

    return {"video_id": video_id}


@celery.task(bind=True)
def text_from_frames(self, input, **kwargs):
    video_id = input["video_id"]
    video = get_video_by_id(video_id=video_id)
    frames_text = analyze_frames(video.video_path)

    update_video(video_id=video_id, status="FRAMES_DESCRIBED", frames_text=frames_text)

    return {
        "video_id": video_id,
    }


@celery.task(bind=True)
def process_video_text(self, input, **kwargs):
    video_id = input["video_id"]
    video = get_video_by_id(video_id=video_id)
    frames_text = video.frames_text
    logger.info(f"Processing video with model for video with id: {video_id}")

    video = get_video_by_id(video_id=video_id)
    prediction = predict_video(
        lm,
        nested_taxonomy,
        VideoFeatures(
            video_id=video_id,
            title=video.title,
            description=video.description,
            video_desc=frames_text,
            s2t=video.text,
        ),
    )
    logger.info(f"Processed video for video with id: {video_id}")
    logger.info(f"Predicted tags for video: {video_id} {str(prediction)}")

    update_video(
        video_id=video_id,
        status="MODEL_PROCESSED",
        tags=f'[{",".join(prediction["predicted_tags"])}]',
    )

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
