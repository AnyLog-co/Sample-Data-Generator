#!/bin/bash

if [[ ${PERFORMANCE_TESTING} == true ]]
then
  if [[ ${EXCEPTION} == true ]] && [[ ${COMPRESS} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress \
      --exception
  elif [[ ${EXCEPTION} == false ]] && [[ ${COMPRESS} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress
  elif [[ ${EXCEPTION} == true ]] && [[ ${COMPRESS} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --exception
  elif [[ ${EXCEPTION} == false ]] && [[ ${COMPRESS} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --performance-testing \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data
  fi
else
  if [[ ${EXCEPTION} == true ]] && [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${COMPRESS} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress \
      --exception
  elif [[ ${EXCEPTION} == true ]] && [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${COMPRESS} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --exception
  elif [[ ${EXCEPTION} == false ]] && [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${COMPRESS} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress
  elif [[ ${EXCEPTION} == false ]] && [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${COMPRESS} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data
  elif [[ ${EXCEPTION} == true ]] && [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${COMPRESS} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress \
      --exception
  elif [[ ${EXCEPTION} == true ]] && [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${COMPRESS} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --exception
  elif [[ ${EXCEPTION} == false ]] && [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${COMPRESS} == true ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data \
      --compress
  elif [[ ${EXCEPTION} == false ]] && [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${COMPRESS} == false ]]
  then
    python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --dir-name ${ANYLOG_PATH}/Sample-Data-Generator/data
  fi

fi
