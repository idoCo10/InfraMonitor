FROM python:3.12-slim

ARG INFRAMONITOR_VERSION
ARG INFRAMONITOR_BUILD_TIME

ENV INFRAMONITOR_VERSION=${INFRAMONITOR_VERSION}
ENV INFRAMONITOR_BUILD_TIME=${INFRAMONITOR_BUILD_TIME}

WORKDIR /app

COPY pyproject.toml .
COPY alembic.ini .
COPY migrations ./migrations
COPY agent ./agent
COPY backend ./backend

RUN python -m pip install --no-cache-dir ".[backend]"

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && exec python -m uvicorn inframonitor_api.main:app --app-dir backend --host 0.0.0.0 --port 8000"]
