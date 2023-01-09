#!/bin/bash

if [[ ${EXCEPTION} == true ]] && [[ -z ${TABLE_NAME} ]]
then
  if [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == true ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --enable-timezone-range \
      --performance-testing \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == true ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --performance-testing \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == false ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --enable-timezone-range \
      --exception
  else
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --exception
  fi
elif [[ ${EXCEPTION} == false ]] && [[ -z ${TABLE_NAME} ]]
then
  if [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == true ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --enable-timezone-range \
      --performance-testing \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == true ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --performance-testing
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == false ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --enable-timezone-range
  else
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE}
  fi
elif [[ ${EXCEPTION} == true ]];
then
  if [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == true ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --enable-timezone-range \
      --performance-testing \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == true ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --performance-testing \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == false ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --enable-timezone-range \
      --exception
  else
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --exception
  fi
elif [[ ${EXCEPTION} == false ]] ;
then
  if [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == true ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --enable-timezone-range \
      --performance-testing \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == true ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --performance-testing
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == false ]]
  then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir ${DATA_DIR} \
      --enable-timezone-range
  else
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE}
  fi
fi