#!/bin/bash

CMD="python3 $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME}"

if [[ ${EXTENDED_HELP} == true ]]; then
  CMD+=" --extended-help"
  bash -c "${CMD}"
  exit 1
elif [[ ${HELP} == true ]] || [[ -z ${DATA_TYPE}  ]] || [[ -z ${INSERT_PROCESS} ]] || [[ -z ${DB_NAME} ]]; then
  CMD+=" --help"
  bash -c "${CMD}"
  exit 1

fi

if [[ -n ${TABLE_NAME} ]] ; then CMD+=" --table-name ${TABLE_NAME}" ; fi
if [[ -n ${TOTAL_ROWS} ]] ; then CMD+=" --total-rows ${TOTAL_ROWS}" ; fi
if [[ -n ${BATCH_SIZE} ]] ; then CMD+=" --batch-size ${BATCH_SIZE}" ; fi
if [[ -n ${SLEEP} ]] ; then CMD+=" --sleep ${SLEEP}" ; fi
if [[ -n ${CONN} ]] ; then CMD+=" --conn ${CONN}" ; fi
if [[ -n ${TOPIC} ]] ; then CMD+=" --topic ${TOPIC}"; fi
if [[ -n ${REST_TIMEOUT} ]] ; then CMD+=" --rest-timeout ${REST_TIMEOUT}" ; fi
if [[ -n ${QOS} ]] ; then CMD+=" --qos ${QOS}" ; fi

if [[ -n ${TIMEZONE} ]] ; then CMD+=" --timezone ${TIMEZONE}" ; fi
if [[ ${ENABLE_TIMEZONE_RANGE} == true ]] ; then CMD+=" --enable-timezone-range"; fi
if [[ ${PERFORMANCE_TESTING} == true ]] ; then CMD+=" --performance-testing"; fi
if [[ ${COMPRESS} == true ]] ; then CMD+=" --compress"; fi
if [[ ${EXCEPTION} == true ]] ; then CMD+=" --exception" ; fi

bash -c "${CMD}"