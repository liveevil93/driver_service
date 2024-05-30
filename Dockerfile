FROM python:3.11.8-alpine as python

FROM python as python-lib-stage
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# poetry:

ENV POETRY_VIRTUALENVS_CREATE false
ENV POETRY_CACHE_DIR '/var/cache/pypoetry'

WORKDIR ${APP_HOME}

# System deps:
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev postgresql-dev libffi-dev bash

FROM python-lib-stage as python-deps-stage

RUN pip install --upgrade pip==23.3
RUN pip install poetry

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry install

FROM python-deps-stage as python-copy-stage

COPY . ${APP_HOME}
RUN pip3 install uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]