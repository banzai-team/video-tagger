from fastapi import FastAPI, status, File, Form, UploadFile
from typing import Annotated

from fastapi.responses import JSONResponse
from app.apis import v1_router
from app.logger import logger
from app.db import engine
from app.db import video  # Import your models

# Create database tables
# video.Base.metadata.create_all(bind=engine)

from app.apis import v1_router

from app.logger import logger
from app.celery_worker import process_video_tags_for_url, process_video_tags_for_file

app = FastAPI(title="ml service", description="Fastapi service for gk", version="0.1")

# Adding v1 namespace route
app.include_router(v1_router)
logger.info("router add succeed")


@app.get("/health", tags=["System probs"])
def health() -> int:
    return status.HTTP_200_OK


@app.get("/api/video/{id}", tags=["System probs"])
def health() -> int:
    return status.HTTP_200_OK


@app.post("/api/video/analyze-tags")
def analyze_video(
    url: str = None,
    title: Annotated[str, Form()] = None,
    file: UploadFile | None = None,
) -> JSONResponse:
    logger.info(f"{url} ... {title} ... {file.filename}")
    if id is None and file is None:
        return status.HTTP_400_BAD_REQUEST

    if file is not None:
        if title is None or title == "":
            return JSONResponse(
                {"info": f"Title must be specified."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        contents = file.file.read()
        process_video_tags_for_file(title, contents)
    else:
        process_video_tags_for_url(url)

    return JSONResponse(
        content={
            "info": f"File '{title if file is not None else url}' is being processed."
        },
        status_code=status.HTTP_201_CREATED,
    )
