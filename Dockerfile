FROM python:3.9-alpine as base

WORKDIR /app
RUN mkdir -p /app/Sample-Data-Generator/blobs \
    /app/Sample-Data-Generator/data_generator \
    /app/Sample-Data-Generator/data_publisher

COPY blobs/* /app/Sample-Data-Generator/blobs
COPY data_generator/* /app/Sample-Data-Generator/data_generator
COPY data_publisher/* /app/Sample-Data-Generator/data_generator
COPY requirements.txt /app/Sample-Data-Generator/requirements.txt
COPY data_generator.py /app/Sample-Data-Generator/data_generator.py
COPY data_generator.sh /app/Sample-Data-Generator/data_generator.sh

RUN apk update && apk upgrade && \
    apk add bash python3 python3-dev py3-pip && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r /app/Sample-Data-Generator/requirements.txt

FROM base AS deployment
ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT bash /app/Sample-Data-Generator/data_generator.sh
