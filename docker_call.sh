#!/bin/bash
if [[ ${INSERT_PROCESS} == file ]] ; then
  if [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == true ]] && [[ ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --performance-testing \
      --compress \
      --exception
  elif [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == true ]] && [[ ! ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --performance-testing \
      --exception
  elif [[ ${PERFORMANCE_TESTING} == true ]] && [[ ! ${EXCEPTION} == true ]] && [[ ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --performance-testing \
      --compress
  elif [[ ${PERFORMANCE_TESTING} == true ]] && [[ ! ${EXCEPTION} == true ]] && [[ ! ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --performance-testing
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${EXCEPTION} == true ]] && [[ ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --enable-timezone-range \
      --compress \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${EXCEPTION} == true ]] && [[ ! ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --enable-timezone-range \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ! ${EXCEPTION} == true ]] && [[ ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --enable-timezone-range \
      --compress
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ! ${EXCEPTION} == true ]] && [[ ! ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --enable-timezone-range
  elif [[ ${EXCEPTION} == true ]] && [[ ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --compress \
      --exception
  elif [[ ! ${EXCEPTION} == true ]] && [[ ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --compress
  elif [[ ${EXCEPTION} == true ]] && [[ ! ${COMPRESS} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data \
      --exception
    else
      python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --data-dir $ANYLOG_PATH/data
    fi
elif [[ ${INSERT_PROCESS} == print ]] ; then
  if [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --performance-testing \
      --exception
  elif [[ ${PERFORMANCE_TESTING} == true ]] && [[ ! ${EXCEPTION} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --performance-testing
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${EXCEPTION} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ! ${EXCEPTION} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range
  elif [[ ${EXCEPTION} == true ]] ; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --exception
  else
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE}
    fi
else
  if [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == true ]] ; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --rest_timeout=${REST_TIMEOUT} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --performance-testing \
      --exception
  elif [[ ${PERFORMANCE_TESTING} == true ]] && [[ ! ${EXCEPTION} == true ]] ; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --rest_timeout=${REST_TIMEOUT} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --performance-testing
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${EXCEPTION} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --rest_timeout=${REST_TIMEOUT} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range \
      --exception
  elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ! ${EXCEPTION} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --rest_timeout=${REST_TIMEOUT} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --enable-timezone-range
  elif [[ ${EXCEPTION} == true ]]; then
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --rest_timeout=${REST_TIMEOUT} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE} \
      --exception
  else
    python3.9 $ANYLOG_PATH/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
      --conn ${CONN} \
      --topic ${TOPIC} \
      --rest_timeout=${REST_TIMEOUT} \
      --table-name ${TABLE_NAME} \
      --total-rows ${TOTAL_ROWS} \
      --batch-size ${BATCH_SIZE} \
      --sleep ${SLEEP} \
      --timezone ${TIMEZONE}
  fi

fi
