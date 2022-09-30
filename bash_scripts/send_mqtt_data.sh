#!/bin/bash

if [[ ${PERFORMANCE_TESTING} == true ]]
then
  if [[ ${EXCEPTION} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --exception
  elif [[ ${EXCEPTION} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --conn ${CONN} \
      --topic ${TOPIC}
  fi
else
  if [[ ${EXCEPTION} == true ]] && [[ ${ENABLE_TIMEZONE_RANGE} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --exception
  elif [[ ${EXCEPTION} == false ]] && [[ ${ENABLE_TIMEZONE_RANGE} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --conn ${CONN} \
      --topic ${TOPIC}
  elif [[ ${EXCEPTION} == true ]] && [[ ${ENABLE_TIMEZONE_RANGE} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --exception
  elif [[ ${EXCEPTION} == false ]] && [[ ${ENABLE_TIMEZONE_RANGE} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --conn ${CONN} \
      --topic ${TOPIC}
  fi
fi
