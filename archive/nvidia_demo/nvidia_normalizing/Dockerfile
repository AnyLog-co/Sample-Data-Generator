FROM ubuntu:20.04

# declare params
ENV ROOT_DIR=/app
ENV DEBIAN_FRONTEND=noninteractive

COPY . nvidia_normalizing
WORKDIR $ROOT_DIR

# update / upgrade
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y update

# install requirements via apt
RUN apt-get -y install wget unzip
RUN apt-get -y install python3.9 python3-pip
RUN apt-get -y install libpq-dev python3.9-dev
RUN python3.9 -m pip install --upgrade pip

RUN python3.9 -m pip install requests
RUN python3.9 -m pip install paho-mqtt

# NGC install
RUN wget -O ngccli_linux.zip https://ngc.nvidia.com/downloads/ngccli_linux.zip 
RUN unzip -o ngccli_linux.zip
RUN  chmod u+x ngc
RUN md5sum -c ngc.md5
RUN echo "export PATH=\"\$PATH:$(pwd)\"" >> ~/.bash_profile
RUN . ~/.bash_profile
#CMD ["/bin/bash -c", "source ~/.bash_profile"]
RUN apt-get -y update



