#!/bin/bash
celery -A app.tasks worker --loglevel=info &
uvicorn app.main:app --host 0.0.0.0 --port 8080
