FROM python:3.9-alpine as base

WORKDIR /app
RUN mkdir -p /app/Sample-Data-Generator/blobs \
    /app/Sample-Data-Generator/blobs/car_video \
    /app/Sample-Data-Generator/blobs/factory_images \
    /app/Sample-Data-Generator/blobs/people_video \
    /app/Sample-Data-Generator/blobs/models \
    /app/Sample-Data-Generator/data_generator \
    /app/Sample-Data-Generator/data_publisher

COPY blobs/car_video /app/Sample-Data-Generator/blobs/car_video
COPY blobs/factory_images /app/Sample-Data-Generator/blobs/factory_images
COPY blobs/people_video /app/Sample-Data-Generator/blobs/people_video
COPY blobs/models /app/Sample-Data-Generator/blobs/models
COPY blobs/factory_images.json /app/Sample-Data-Generator/blobs/factory_images.json

COPY data_generator/* /app/Sample-Data-Generator/data_generator
COPY data_publisher/* /app/Sample-Data-Generator/data_publisher
COPY requirements.txt /app/Sample-Data-Generator/requirements.txt
COPY data_generator.py /app/Sample-Data-Generator/data_generator.py
COPY data_generator.sh /app/Sample-Data-Generator/data_generator.sh

RUN apk update && apk upgrade && \
    apk add bash python3 python3-dev py3-pip && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r /app/Sample-Data-Generator/requirements.txt

FROM base AS deployment
#ENTRYPOINT ["/bin/bash"]
ENTRYPOINT bash /app/Sample-Data-Generator/data_generator.sh
