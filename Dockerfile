# docker buildx build . --platform linux/amd64,linux/arm64 -t anylogco/sample-data-generator:cpu-test --push
FROM ubuntu:22.04 as base

WORKDIR /app/Sample-Data-Generator
RUN mkdir data_publisher  data_generator blobs
COPY data_publisher/* data_publisher/
COPY data_generator/* data_generator/
COPY blobs/* blobs/
COPY requirements.txt requirements.txt
COPY main.py main.py

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install python3-pip && \
    apt-get -y install python3-flask && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade requirements.txt || true

FROM base as deployment

WORKDIR /app
COPY main.sh /app/main.sh

ENV VIEW_HELP=false \
    DATA_TYPE=rand \
    PUBLISHER=server \
    DB_NAME=test \
    TOPIC=test \
    REST_CONN=127.0.0.1:32149 \
    BATCH_SIZE=10 \
    TOTAL_ROWS=10 \
    SLEEP=0.5 \
    TIMEOUT=30 \
    QOS=0 \
    SERVICE_PORT=8481 \
    CREATE_LARGE_DATA=false

ENTRYPOINT ["/bin/bash", "/app/main.sh"]
