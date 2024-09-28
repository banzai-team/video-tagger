from typing import List
from fastapi import status
from fastapi.routing import APIRouter

from .model import InputCl, OutputCl

router = APIRouter(prefix="/v1")


from fastapi import UploadFile, File, Form
from pydantic import BaseModel, HttpUrl
from app.celery_worker import process_video_tags_for_url, process_video_tags_for_file
from app.logger import logger
from fastapi.responses import JSONResponse
from app.db.engine import get_db
from app.db.video import Status, Video


class VideoUrlInput(BaseModel):
    video_url: HttpUrl


class VideoFileInput(BaseModel):
    description: str
    title: str


class TaskOutput(BaseModel):
    task_id: str


class VideoRepr(BaseModel):
    id: int
    status: str
    title: str
    description: str | None = None
    url: str | None = None
    file_path: str | None = None
    tags: str | None = None
    video_path: str | None = None
    text: str | None = None
    audio_path: str | None = None
    url: str | None = None


@router.post(
    "/process_video_url",
    description="Обрабатывает видео по URL",
    tags=["Inference endpoints"],
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TaskOutput,
)
def process_video_url(input_data: VideoUrlInput) -> TaskOutput:
    # Здесь должна быть логика создания задачи для обработки видео по URL
    logger.info(f"Received process_video_url request for url: {input_data.video_url}")
    if id is None and file is None:
        return status.HTTP_400_BAD_REQUEST

    task_id = process_video_tags_for_url(str(input_data.video_url))
    print(str(task_id))
    return TaskOutput(task_id="22")


@router.post(
    "/process_video_file",
    description="Обрабатывает загруженное видео",
    tags=["Inference endpoints"],
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TaskOutput,
)
async def process_video_file(
    file: UploadFile = File(...), description: str = Form(...), title: str = Form(...)
) -> TaskOutput:
    # Здесь должна быть логика создания задачи для обработки загруженного видео
    if title is None or title == "":
        return JSONResponse(
            {"info": f"Title must be specified."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    contents = file.file.read()
    task_id = process_video_tags_for_file(title, description, contents)
    print(str(task_id))

    return TaskOutput(task_id="222")


@router.get(
    "/videos/{id}",
    description="Получает видео по идентфиикатору",
    tags=["Inference endpoints"],
    status_code=status.HTTP_200_OK,
    response_model=VideoRepr,
)
def get_video_by_id(id):
    db = next(get_db())
    video = db.query(Video).filter(Video.id == id).first()
    if video is None:
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)
    return video_to_repr(video)


@router.get(
    "/videos",
    description="Получает список видео",
    tags=["Inference endpoints"],
    status_code=status.HTTP_200_OK,
    response_model=List[VideoRepr],
)
def get_videos(skip=0, size=10) -> int:
    db = next(get_db())
    res = db.query(Video).limit(size).offset(skip)
    return [video_to_repr(item) for item in res]


def video_to_repr(video):
    return VideoRepr(
        id=video.id,
        status=video.status,
        title=video.title,
        description=video.description,
        video_path=video.video_path,
        audio_path=video.audio_path,
        text=video.text,
        tags=video.tags,
        url=video.url,
    )
