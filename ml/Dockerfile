FROM python:3.11-slim as base

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends build-essential gcc-11 g++-11 clang ffmpeg git

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # env
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

FROM base
#
ADD ./app ./app
ADD ./data ./data
#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]