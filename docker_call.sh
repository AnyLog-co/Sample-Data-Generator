if [[ -z ${TABLE_NAME} ]] ; then TABLE_NAME="" ; fi
if [[ -z ${TOTAL_ROWS} ]] ; then TOTAL_ROWS=1000000 ; fi
if [[ -z ${BATCH_SIZE} ]] ; then BATCH_SIZE=1000 ; fi
if [[ -z ${SLEEP} ]] ; then SLEEP=0.5 ; fi
if [[ -z ${TIMEZONE} ]] ; then TIMEZONE=local ; fi
if [[ -z ${CONN} ]] ; then CONN="" ; fi
if [[ -z ${TOPIC} ]] ; then TOPIC="" ; fi
if [[ -z ${REST_TIMEOUT} ]] ; then REST_TIMEOUT=30 ; fi
if [[ -z ${DIR_NAME} ]] ; then DIR_NAME=$ANYLOG_PATH/Sample-Data-Generator/data ; fi

if [[ ! ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ! ${ENABLE_TIMEZONE_RANGE} == false ]] ; then ENABLE_TIMEZONE_RANGE=false ; fi
if [[ ! ${PERFORMANCE_TESTING} == true ]] && [[ ! ${PERFORMANCE_TESTING} == false ]] ; then PERFORMANCE_TESTING=false ; fi
if [[ ! ${COMPRESS} == true ]] && [[ ! ${COMPRESS} == false ]] ; then COMPRESS=false ; fi
if [[ ! ${EXCEPTION} == true ]] && [[ ! ${EXCEPTION} == false ]] ; then EXCEPTION=false ; fi

if [[ ${INSERT_PROCESS} == print ]] ; then
  bash $ANYLOG_PATH/Sample-Data-Generator/docker_scripts/data_generataor_generic_print.sh
elif [[ ${INSERT_PROCESS} == file ]] && [[ ${COMPRESS} == true ]] ; then
  bash $ANYLOG_PATH/Sample-Data-Generator/docker_scripts/data_generataor_generic_file_compress.sh
elif [[ ${INSERT_PROCESS} == file ]] && [[ ${COMPRESS} == false ]] ; then
  bash $ANYLOG_PATH/Sample-Data-Generator/docker_scripts/data_generataor_generic_file.sh
elif [[ ! ${INSERT_PROCESS} == file ]] && [[ ! ${INSERT_PROCESS} == print ]] ; then
  if [[ ! ${CONN} ]] ; then
    echo "Missing connection credentials, cannot continue"
    exit 1
  fi
  if [[ ! ${INSERT_PROCESS} == put ]] && [[ -z ${TOPIC} ]] ;
  then
    echo "Missing `topic` value for ${INSERT_PROCESS} insert process, cannot continue"
    exit 1
  fi
elif [[ ${INSERT_PROCESS} == put ]] ; then
  bash $ANYLOG_PATH/Sample-Data-Generator/docker_scripts/data_generataor_generic_rest_put.sh
elif [[ ${INSERT_PROCESS} == put ]] ; then
  bash $ANYLOG_PATH/Sample-Data-Generator/docker_scripts/data_generataor_generic_post_mqtt.sh
fi

#if [[ ${INSERT_PROCESS} == put ]] ; then bash $ANYLOG_PATH/Sample-Data-Generator/docker_scripts/run_put.sh ; fi
#if [[ ${INSERT_PROCESS} == post ]] || [[ ${INSERT_PROCESS} == mqtt ]] ; then bash $ANYLOG_PATH/Sample-Data-Generator/docker_scripts/run_post_mqtt.sh ; fi

