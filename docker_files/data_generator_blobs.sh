#!/bin/bash

CMD="python3 $ANYLOG_ROOT_DIR/Sample-Data-Generator/data_generator_blobs.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME}"

if [[ ${EXTENDED_HELP} == true ]]; then
  CMD+=" --extended-help"
  bash -c "${CMD}"
  exit 1
elif [[ ${HELP} == true ]] || [[ -z ${DATA_TYPE}  ]] || [[ -z ${INSERT_PROCESS} ]] || [[ -z ${DB_NAME} ]]; then
  CMD+=" --help"
  bash -c "${CMD}"
  exit 1

fi

if [[ -n ${CONVERSTION_TYPE} ]] ; then CMD+=" --conversion-type ${CONVERSION_TYPE}" ; fi
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
if [[ ${REMOTE_DATA} == true ]] ; then CMD+= " --remote-data" ; fi
if [[ -n ${URL} ]] ; then CMD+=" --url ${URL}" ; fi
if [[ -n ${API_KEY} ]] ; then CMD+=" --api-key ${API_KEY}" ; fi
if [[ -n ${AUTHENTICATION} ]] ; then CMD+=" --authentication ${AUTHENTICATION}" ; fi
if [[ ${EXCEPTION} == true ]] ; then CMD+=" --exception" ; fi

bash -c "${CMD}"