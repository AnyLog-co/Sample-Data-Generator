FROM ubuntu:18.04

# declare params 
ARG ANYLOG_ROOT_DIR=/app

# update / upgrade 
RUN apt-get -y update 	
RUN apt-get -y upgrade 
RUN apt-get -y update	

# install requirements via apt 
RUN apt-get -y install python3 python3-pip
RUN pip3 install --upgrade pip

# install requirements via pip 
RUN python3 -m pip install requests
RUN python3 -m pip install pytz
RUN python3 -m pip install paho-mqtt
RUN python3 -m pip install tzlocal


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

ENTRYPOINT bash /app/Sample-Data-Generator/docker_call.sh
 
