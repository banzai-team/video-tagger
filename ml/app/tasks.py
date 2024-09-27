import time
from celery import Celery
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

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


@celery.task(bind=True)
def process_video(self, video_id):
    # Simulating video processing
    for i in range(100):
        self.update_state(state="PROGRESS", meta={"progress": i})
        time.sleep(0.1)
    return {"status": "completed"}
