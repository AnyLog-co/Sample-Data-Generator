#!/bin/bash

if [[ ${PERFORMANCE_TESTING} -eq true ]]
then
  if [[ ${EXCEPTION} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --conn ${CONN} \
      --rest-timeout ${REST_TIMEOUT} \
      --exception
  elif [[ ${EXCEPTION} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --conn ${CONN} \
      --rest-timeout ${REST_TIMEOUT} \
  fi
else
  if [[ ${EXCEPTION} -eq true ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --conn ${CONN} \
      --rest-timeout ${REST_TIMEOUT} \
      --exception
  elif [[ ${EXCEPTION} -eq false ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --conn ${CONN} \
      --rest-timeout ${REST_TIMEOUT} \
  elif [[ ${EXCEPTION} -eq true ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --conn ${CONN} \
      --rest-timeout ${REST_TIMEOUT} \
      --exception
  elif [[ ${EXCEPTION} -eq false ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --conn ${CONN} \
      --rest-timeout ${REST_TIMEOUT}
  fi
fi
