FROM python:3.9-slim as develop

ENV EDITOR="vim"

RUN python3.9 -m pip install --upgrade pip && \
    python3.9 -m pip install poetry \
    || exit 1

RUN apt-get update && \
    apt-get install -y vim texlive-latex-recommended make

RUN mkdir /walden
WORKDIR /workspace
COPY ./poetry.lock /workspace/poetry.lock
COPY ./pyproject.toml /workspace/pyproject.toml
COPY ./README.md /workspace/README.md
COPY ./LICENSE /workspace/LICENSE
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . /workspace
RUN poetry install
