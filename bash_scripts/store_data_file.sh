#!/bin/bash

if [[ ${PERFORMANCE_TESTING} -eq true ]]
then
  if [[ ${EXCEPTION} -eq true ]] && [[ ${COMPRESS} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress \
      --exception
  elif [[ ${EXCEPTION} -eq false ]] && [[ ${COMPRESS} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress
  elif [[ ${EXCEPTION} -eq true ]] && [[ ${COMPRESS} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --exception
    elif [[ ${EXCEPTION} -eq false ]] && [[ ${COMPRESS} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data
  fi
else
  if [[ ${EXCEPTION} -eq true ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq true ]] && [[ ${COMPRESS} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress \
      --exception
  elif [[ ${EXCEPTION} -eq true ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq true ]] && [[ ${COMPRESS} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --exception
  elif [[ ${EXCEPTION} -eq false ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq true ]] && [[ ${COMPRESS} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress
  elif [[ ${EXCEPTION} -eq false ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq true ]] && [[ ${COMPRESS} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data
  elif [[ ${EXCEPTION} -eq true ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq false ]] && [[ ${COMPRESS} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress \
      --exception
  elif [[ ${EXCEPTION} -eq true ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq false ]] && [[ ${COMPRESS} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --exception
  elif [[ ${EXCEPTION} -eq false ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq false ]] && [[ ${COMPRESS} -eq true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress
  elif [[ ${EXCEPTION} -eq false ]] && [[ ${ENABLE_TIMEZONE_RANGE} -eq false ]] && [[ ${COMPRESS} -eq false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${ANYLOG_PATH}/Sample-Data-Generator/data
  fi

fi
