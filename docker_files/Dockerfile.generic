FROM python:3.10-alpine

# declare params
ENV ANYLOG_ROOT_DIR=/app

# update / upgrade
RUN apk update && apk upgrade

# install requirements via apk
RUN apk add --no-cache postgresql-dev
RUN apk add bash

# move to WORKDIR + COPY codebase
WORKDIR $ANYLOG_ROOT_DIR
RUN mkdir -p $ANYLOG_ROOT_DIR/Sample-Data-Generator
COPY data_generators $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/data_generator_images.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/data_generator_videos.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/edgex_data.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/live_feed.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/nvidia_read_logs.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/transit_data.py

COPY publishing_protocols $ANYLOG_ROOT_DIR/Sample-Data-Generator/publishing_protocols
COPY data_generator_generic.py $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generator_generic.py
COPY docker_files/data_generator_generic.sh $ANYLOG_ROOT_DIR/Sample-Data-Generator/docker_call.sh

# configure usr
RUN chmod 777 $ANYLOG_ROOT_DIR
RUN chmod -R 755 $ANYLOG_ROOT_DIR/Sample-Data-Generator

# install requirements via pip
RUN pip install --upgrade pip
RUN pip install --upgrade argparse>=0.0 || true
RUN pip install --upgrade datetime>=0.0 || true
RUN pip install --upgrade geopy>=0.0 || true
RUN pip install --upgrade gzip>=0.0 || true
RUN pip install --upgrade io>=0.0 || true
RUN pip install --upgrade json>=0.0 || true
RUN pip install --upgrade math>=0.0 || true
RUN pip install --upgrade os>=0.0 || true
RUN pip install --upgrade paho-mqtt>=0.0 || true
RUN pip install --upgrade pytz>=0.0 || true
RUN pip install --upgrade random>=0.0 || true
RUN pip install --upgrade requests>=0.0 || true
RUN pip install --upgrade sys>=0.0 || true
RUN pip install --upgrade time>=0.0 || true
RUN pip install --upgrade uuid>=0.0 || true
#RUN pip install --upgrade base64>=0.0 || true
#RUN pip install --upgrade opencv-python>=0 || true
#RUN pip install --upgrade numpy>=0.0 || true

ENTRYPOINT /bin/bash
#ENTRYPOINT bash $ANYLOG_ROOT_DIR/Sample-Data-Generator/docker_call.sh
