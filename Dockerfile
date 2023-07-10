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
COPY . Sample-Data-Generator

# configure usr
RUN chmod -R 777 $ANYLOG_ROOT_DIR
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
RUN pip install --upgrade base64>=0.0 || true
RUN pip install --upgrade opencv-python>=0 || true
RUN pip install --upgrade numpy>=0.0 || true

#RUN python3 -m pip install --no-cache-dir -r $ANYLOG_ROOT_DIR/Sample-Data-Generator/requirements.txt || true

ENTRYPOINT bash $ANYLOG_ROOT_DIR/Sample-Data-Generator/docker_call.sh