from fastapi import FastAPI, status, File, Form, UploadFile

from app.apis import v1_router
from app.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Create database tables
# video.Base.metadata.create_all(bind=engine)

from app.apis import v1_router

from app.logger import logger

app = FastAPI(title="ml service", description="Fastapi service for gk", version="0.1")

# Adding v1 namespace route
app.include_router(v1_router)
logger.info("router add succeed")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")


@app.get("/health", tags=["System probs"])
def health() -> int:
    return status.HTTP_200_OK
