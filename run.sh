#!/bin/bash

if [[ ${HELP} == true ]] || [[ -z ${DATA_TYPE}  ]] || [[ -z ${INSERT_PROCESS} ]] || [[ -z ${DB_NAME} ]]; then
  CMD+=" --help"
  bash -c "${CMD}"
  exit 1
fi

chmod +x $APP_DIR/dist/sample_data_generator_x86_64_v1.3.2401

CMD="python3 $ANYLOG_ROOT_DIR/Sample-Data-Generator/sample_data_generator.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME}"


if [[ ${DATA_TYPE} == images ]] || [[ ${DATA_TYPE} == cars ]] && [[ ${DATA_TYPE} == people ]] ; then CMD+="--conversion-type ${CONVERSTAION_TYPE}" ; fi

if [[ -n ${TOTAL_ROWS} ]] ; then CMD+=" --total-rows ${TOTAL_ROWS}" ; fi
if [[ -n ${BATCH_SIZE} ]] ; then CMD+=" --batch-size ${BATCH_SIZE}" ; fi
if [[ -n ${SLEEP} ]] ; then CMD+=" --sleep ${SLEEP}" ; fi
if [[ -n ${CONN} ]] ; then CMD+=" --conn ${CONN}" ; fi
if [[ -n ${TOPIC} ]] ; then CMD+=" --topic ${TOPIC}"; fi
if [[ -n ${REST_TIMEOUT} ]] ; then CMD+=" --rest-timeout ${REST_TIMEOUT}" ; fi
if [[ -n ${QOS} ]] ; then CMD+=" --qos ${QOS}" ; fi

if [[ -n ${TIMEZONE} ]] ; then CMD+=" --timezone ${TIMEZONE}" ; fi
if [[ ${ENABLE_TIMEZONE_RANGE} == true ]] ; then CMD+=" --enable-timezone-range"; fi
if [[ ${DIR_NAME} == true ]] ; then CMD+=" --dir-name ${DIR_NAME}"; fi
if [[ ${EXCEPTION} == true ]] ; then CMD+=" --exception" ; fi


# install programs
if [[ ${INSERT_PROCESS} == mqtt ]] ; then
  python3 -m pip install paho-mqtt
fi
if [[ ${DATA_TYPE} == edgex ]] || [[ ${DATA_TYPE} == video ]] ; then
  python3 -m pip install --upgrade numpy opencv-python
  python3 -m pip install tensorflow numpy
elif [[ ${CONVERSION_TYPE} == opencv ]] ; then
  python3 -m pip install --upgrade opencv-python numpy
fi

# Validate values
if [[ ${DATA_TYPE} == node_insight ]] && [[ ${INSERT_PROCESS} == mqtt ]] ; then
  echo "node_insight requires using REST for data processing"
  exit 1
fi

bash -c "${CMD}"