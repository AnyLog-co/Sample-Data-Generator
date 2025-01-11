#!/bin/bash

echo ${VIEW_HELP}
if [[ ${VIEW_HELP} == true ]] ; then
    python3 /app/Sample-Data-Generator/main.py --help
elif [[ ${CREATE_LARGE_DATA} == true ]] && [[ ${EXCEPTION} == true ]]; then
    python3 /app/Sample-Data-Generator/main.py ${DATA_TYPE} ${PUBLISHER} ${DB_NAME} \
        --rest-conn ${REST_CONN} \
        --batch-size ${BATCH_SIZE} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --topic ${TOPIC} \
        --timeout ${TIMEOUT} \
        --qos ${QOS} \
        --service-port ${SERVICE_PORT} \
        --create-large-data \
        --num-tables ${NUM_TABLES} \
        --num-columns ${NUM_COLUMNS} \
        --exception
elif [[ ${CREATE_LARGE_DATA} == true ]] ; then
    python3 /app/Sample-Data-Generator/main.py ${DATA_TYPE} ${PUBLISHER} ${DB_NAME} \
        --rest-conn ${REST_CONN} \
        --batch-size ${BATCH_SIZE} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --topic ${TOPIC} \
        --timeout ${TIMEOUT} \
        --qos ${QOS} \
        --service-port ${SERVICE_PORT} \
        --create-large-data \
        --num-tables ${NUM_TABLES} \
        --num-columns ${NUM_COLUMNS}
elif [[ ${EXCEPTION} == true ]]; then
    python3 /app/Sample-Data-Generator/main.py ${DATA_TYPE} ${PUBLISHER} ${DB_NAME} \
        --rest-conn ${REST_CONN} \
        --batch-size ${BATCH_SIZE} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --topic ${TOPIC} \
        --timeout ${TIMEOUT} \
        --qos ${QOS} \
        --service-port ${SERVICE_PORT} \
        --exception
else
    python3 /app/Sample-Data-Generator/main.py ${DATA_TYPE} ${PUBLISHER} ${DB_NAME} \
        --rest-conn ${REST_CONN} \
        --batch-size ${BATCH_SIZE} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --topic ${TOPIC} \
        --timeout ${TIMEOUT} \
        --qos ${QOS} \
        --service-port ${SERVICE_PORT}
fi
