FROM python:3.9-slim as develop

RUN apt-get update && \
    apt-get install vim -y

RUN python3.9 -m pip install --upgrade pip && \
    python3.9 -m pip install poetry \
    || exit 1

ENV EDITOR="vim"

COPY . /walden
WORKDIR /walden

RUN poetry config virtualenvs.create false && poetry install
