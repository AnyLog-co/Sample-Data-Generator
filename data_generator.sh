#!/bin/bash


if [[ ! ${DATA_GENERATOR} ]] ; then export DATA_GENERATOR=rand ; fi
if [[ ! ${CONN} ]] ; then export CONN=127.0.0.1:32149 ; fi
if [[ ! ${PUBLISHER} ]] ; then export PUBLISHER=put ; fi
if [[ ! ${BATCH_SIZE} ]] ; then export BATCH_SIZE=10 ; fi
if [[ ! ${TOTAL_ROWS} ]] ; then export TOTAL_ROWS=10 ; fi
if [[ ! ${SLEEP} ]] ; then export SLEEP=0.5 ; fi
if [[ ! ${DB_NAME} ]] ; then export DB_NAME=test ; fi
if [[ ! ${TOPIC} ]] ; then export TOPIC=test ; fi
if [[ ! ${TIMEOUT} ]] ; then export TIMEOUT=30 ; fi
if [[ ! ${QOS} ]] ; then export QOS=0 ; fi
if [[ ! ${EXCEPTION} ]] ; then export EXCEPTION=false ; fi
if [[ ! ${EXAMPLES} ]] ; then EXAMPLES=false ; fi
if [[ ! ${HELP} ]] ; then HELP=false ; fi

if [[ ${HELP} == true  ]] ; then
  python3 /app/Sample-Data-Generator/data_generator.py --help
fi
if [[ ${EXAMPLES} == true ]] ; then
  python3 /app/Sample-Data-Generator/data_generator.py rand 127.0.0.1:32149 put --examples
fi

if [[ ${HELP} == true ]] || [[ ${EXAMPLES} == true ]] ; then
  exit 1
fi

if [[ ${DATA_GENERATOR} == cars ]]; then
  python3 -m pip install --upgrade tensorflow numpy
  apk add --no-cache py3-opencv
fi

if [[ ${PUBLISHER} == mqtt ]]; then
  python3 -m pip install --upgrade paho-mqtt==1.5.1
fi

if [[ ${PUBLISHER} == kafka ]]; then
  python3 -m pip install --upgrade kafka-python
fi

if [[ ${EXCEPTION} == true ]] ; then
  python3 /app/Sample-Data-Generator/data_generator.py ${DATA_GENERATOR} ${CONN} ${PUBLISHER} \
    --db-name ${DB_NAME} \
    --batch-size ${BATCH_SIZE} \
    --total-rows ${TOTAL_ROWS} \
    --sleep ${SLEEP} \
    --topic ${TOPIC} \
    --timeout ${TIMEOUT} \
    --qos ${QOS} \
    --exception
else
    python3 /app/Sample-Data-Generator/data_generator.py ${DATA_GENERATOR} ${CONN} ${PUBLISHER} \
    --db-name ${DB_NAME} \
    --batch-size ${BATCH_SIZE} \
    --total-rows ${TOTAL_ROWS} \
    --sleep ${SLEEP} \
    --topic ${TOPIC} \
    --timeout ${TIMEOUT} \
    --qos ${QOS}
fi