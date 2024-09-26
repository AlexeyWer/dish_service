FROM python:3.12.6-alpine3.20 as base

ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3

RUN apk add --update --no-cache gcc make g++ libffi-dev libpa-dev liblz4-dev libuwind-dev

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv
RUN pip install "typing-extensions>=4.1.0"

COPY pyproject.toml poetry.lock README.md alembic.ini srv/ tests/ migrations/ /app/

CMD ["python", "/app/srv/main.py"]