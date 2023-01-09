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
ENV PERFORMANCE_TESTING=false
ENV CONN=""
ENV TOPIC=""
ENV REST_TIMEOUT=30
ENV COMPRESS=false
ENV EXCEPTION=false

WORKDIR $ANYLOG_PATH
COPY . Sample-Data-Generator

RUN chmod 775 $ANYLOG_PATH

RUN apk update
RUN apk upgrade
RUN apk add bash-completion
RUN apk update

#RUN python3.9 -m pip install --upgrade pip
#RUN python3.9 -m pip install paho-mqtt
#RUN python3.9 -m pip install pytz
#RUN python3.9 -m pip install requests
#
#RUN rm -rf video_processing_demo
#
#RUN mkdir -p $ANYLOG_PATH/Sample-Data-Generator/data
#
#ENTRYPOINT bash $ANYLOG_PATH/Sample-Data-Generator/docker_call.sh