FROM python:3.9-slim as develop

COPY . /walden
WORKDIR /walden

RUN python3.9 -m pip install --upgrade pip && \
    python3.9 -m pip install poetry \
    || exit 1

RUN poetry config virtualenvs.create false && poetry install

