FROM ubuntu:22.04

# declare params
ENV ANYLOG_ROOT_DIR=/app
ENV DEBIAN_FRONTEND=noninteractive

# update / upgrade
RUN apt-get -y update
RUN apt-get -y upgrade 

# install requirements via apk
RUN apt-get -y install python3 python3-pip 
RUN apt-get -y install libpython3-dev 
RUN apt-get -y install pypy3-dev
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0

# move to WORKDIR + COPY codebase
WORKDIR $ANYLOG_ROOT_DIR
RUN mkdir -p $ANYLOG_ROOT_DIR/Sample-Data-Generator
COPY data_generators $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/live_feed.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/lsl_data.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/nvidia_read_logs.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/opcua_data.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/performance_testing.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/power_company.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/transit_data.py
RUN rm -rf $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generators/trig.py

COPY publishing_protocols $ANYLOG_ROOT_DIR/Sample-Data-Generator/publishing_protocols
COPY data_generator_generic_blobs.py $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generator_generic_blobs.py
COPY docker_files/data_generator_blobs.sh $ANYLOG_ROOT_DIR/Sample-Data-Generator/docker_call.sh

COPY data/ntt_factory_data.json $ANYLOG_ROOT_DIR/Sample-Data-Generator/data/ntt_factory_data.json
COPY data/edgex-demo $ANYLOG_ROOT_DIR/Sample-Data-Generator/data/edgex-demo 
COPY data/videos $ANYLOG_ROOT_DIR/Sample-Data-Generator/data/videos 
COPY data/images $ANYLOG_ROOT_DIR/Sample-Data-Generator/data/images 


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
RUN pip install --upgrade base64>=0.0 || true
RUN pip install --upgrade opencv-python>=0 || true
#RUN pip install opencv-python-headless || true
RUN pip install --upgrade numpy>=0.0 || true

#ENTRYPOINT /bin/bash
ENTRYPOINT bash $ANYLOG_ROOT_DIR/Sample-Data-Generator/docker_call.sh
