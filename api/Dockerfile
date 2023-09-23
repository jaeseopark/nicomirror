from python:3.11-slim-bullseye

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/nicomirror

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt
