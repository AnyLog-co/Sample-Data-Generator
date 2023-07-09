FROM ubuntu:20.04

# declare params
ENV ANYLOG_ROOT_DIR=/app
ENV DEBIAN_FRONTEND=noninteractive

# update / upgrade
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y update

# install requirements via apt
RUN apt-get -y install python3.9 python3-pip
RUN apt-get -y install libpq-dev python3.9-dev
RUN apt-get -y install python3-kafka
RUN python3.9 -m pip install --upgrade pip

# move to WORKDIR + COPY codebsae 
WORKDIR $ANYLOG_ROOT_DIR
COPY . Sample-Data-Generator

# configure usr
RUN chmod -R 777 $ANYLOG_ROOT_DIR
RUN chmod -R 755 $ANYLOG_ROOT_DIR/Sample-Data-Generator

# install requirements via pip
RUN python3.10 -m pip install --upgrade -r $ANYLOG_ROOT_DIR/Sample-Data-Generator/requirements.txt || true

RUN apt-get -y update

ENTRYPOINT bash /app/Sample-Data-Generator/docker_call.sh
 
