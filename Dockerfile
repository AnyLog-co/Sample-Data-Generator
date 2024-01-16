FROM python:3.10-alpine

ENV APP_DIR=/app
WORKDIR $APP_DIR

RUN mkdir -p $APP_DIR/Sample-Data-Generator/sample_data_generator
RUN mkdir -p $APP_DIR/Sample-Data-Generator/data

#COPY setup.py $APP_DIR/Sample-Data-Generator/setup.py
#COPY setup.cfg $APP_DIR/Sample-Data-Generator/setup.cfg
COPY run.sh $APP_DIR/Sample-Data-Generator/run.sh
COPY data/* $APP_DIR/Sample-Data-Generator/data
COPY sample_data_generator/* $APP_DIR/Sample-Data-Generator/sample_data_generator

# Install required packages
RUN apk update && \
    apk add build-base libffi-dev  py3-pip python3-dev musl-dev jpeg-dev zlib-dev libressl-dev libwebp-dev libxslt-dev \
     libxml2-dev libpq libstdc++ bash && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade pytz && \
    python3 -m pip install --upgrade requests # && \
#    python3 -m pip install --upgrade Cython && \
#    python3 -m pip install pyinstaller && \
#    python3 $APP_DIR/Sample-Data-Generator/setup.py install
#    rm -rf $APP_DIR/Sample-Data-Generator/src

ENTRYPOINT ["bash", "$APP_DIR/Sample-Data-Generator/run.sh"]
