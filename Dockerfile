FROM python:3.9-slim as develop

ENV EDITOR="vim"

RUN python3.9 -m pip install --upgrade pip && \
    python3.9 -m pip install poetry \
    || exit 1

RUN apt-get update && \
    apt-get install -y vim texlive-latex-recommended make

COPY . /walden
WORKDIR /walden

RUN poetry config virtualenvs.create false && poetry install
