from sqlalchemy import Column, Integer, String, Float, DateTime, func, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class Status(enum.Enum):
    SUBMITTED = "SUBMITTED"
    DOWNLOADING = "DOWNLOADING"
    PROCESSING = "PROCESSING"
    ERROR = "ERROR"


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    video_path = Column(String, nullable=True)
    audio_path = Column(String, nullable=True)
    text = Column(String, nullable=True)
    status = Column(String, default=Status.SUBMITTED)
    progress = Column(Float, default=0.0)
    url = Column(String, nullable=True)  # remote URL
    result = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
