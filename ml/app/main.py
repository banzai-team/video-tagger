from fastapi import FastAPI, status
from app.apis import v1_router
from app.logger import logger
# from app.database import engine
# from app.models import video  # Import your models

# Create database tables
video.Base.metadata.create_all(bind=engine)

from app.apis import v1_router

from app.logger import logger

app = FastAPI(title='ml service',
              description='Fastapi service for gk',
              version='0.1')

# Adding v1 namespace route
app.include_router(v1_router)
logger.info('router add succeed')


@app.get('/health',
         tags=['System probs'])
def health() -> int:
    return status.HTTP_200_OK
