FROM ubuntu:latest	

# declare params 
ARG ANYLOG_ROOT_DIR=/app
ARG ANYLOG_TCP_PORT=$ANYLOG_TCP_PORT 
ARG ANYLOG_TCP_PORT=$ANYLOG_REST_PORT 

# update / upgrade 
RUN apt-get -y update 	
RUN apt-get -y upgrade 
RUN apt-get -y update	

# install requirements via apt 
RUN apt-get -y install curl git

RUN apt-get -y install python3 python3-pip
RUN apt-get -y install python3-psycopg2
RUN pip3 install --upgrade pip

# install requirements via pip 
RUN pip3 install requests
RUN pip3 install psutil

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

 

# Run AnyLog 
ENTRYPOINT bash Sample-Data-Generator/data_generator.sh
