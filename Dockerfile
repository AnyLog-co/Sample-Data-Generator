FROM ubuntu:20.04

# declare params
ENV ANYLOG_ROOT_DIR=/app
ENV DEBIAN_FRONTEND=noninteractive

# update / upgrade
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y update

# install requirements via apt
RUN apt-get -y install curl git
RUN apt-get -y install python3.9 python3-pip
RUN apt-get -y install libpq-dev python3.9-dev
RUN apt-get -y install python3-kafka
RUN python3.9 -m pip install --upgrade pip

# install requirements via pip 
RUN python3.9 -m pip install requests
RUN python3.9 -m pip install pytz
RUN python3.9 -m pip install paho-mqtt
RUN python3.9 -m pip install tzlocal
RUN python3.9 -m pip install kafka-python
RUN apt-get -y update

# Add user 
RUN adduser appuser 

# move to WORKDIR + COPY codebsae 
WORKDIR $ANYLOG_ROOT_DIR
COPY . Sample-Data-Generator

# configure usr 
RUN chown -R appuser:appuser $ANYLOG_ROOT_DIR 
RUN chmod 755 /app

# Swtich user 
USER appuser
RUN apt-get -y update

#ENTRYPOINT bash /app/Sample-Data-Generator/docker_call.sh
 
