FROM python:3.9-alpine

ENV ANYLOG_PATH=/app
ENV DATA_TYPE=trig
ENV INSERT_PROCESS=print
ENV DB_NAME=test
ENV TOTAL_ROWS=1000000
ENV BATCH_SIZE=1000
ENV SLEEP=0.5
ENV TIMEZONE=utc
ENV ENABLE_TIMEZONE_RANGE=false
ENV PERFORMANCE_TESTING=true
ENV CONN=""
ENV TOPIC=""
ENV REST_TIMEOUT=30
ENV DIR_NAME=/app/Sample-Data-Generator/data
ENV COMPRESS=false
ENV EXCEPTION=false


WORKDIR $ANYLOG_PATH
COPY . Sample-Data-Generator

RUN chmod 775 $ANYLOG_PATH

RUN apk update
RUN apk upgrade
RUN apk add bash-completion
RUN apk update

RUN python3.9 -m pip install --upgrade pip
#RUN python3.9 -m pip install gzip
#RUN python3.9 -m pip install math
RUN python3.9 -m pip install paho-mqtt
RUN python3.9 -m pip install pytz
RUN python3.9 -m pip install requests

ENTRYPOINT python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator.py --help