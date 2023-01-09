if [[ -z ${TABLE_NAME} ]] ; then TABLE_NAME="" ; fi
if [[ -z ${TOTAL_ROWS} ]] ; then TOTAL_ROWS=1000000 ; fi
if [[ -z ${BATCH_SIZE} ]] ; then BATCH_SIZE=1000 ; fi
if [[ -z ${SLEEP}]] ; then SLEEP=0.5 ; fi
if [[ -z ${TIMEZONE} ]] ; then TIMEZONE=local ; fi
if [[ -z ${CONN} ]] ; then CONN="" ; fi
if [[ -z ${TOPIC} ]] ; then TOPIC="" ; fi
if [[ -z ${REST_TIMEOUT} ]] ; then REST_TIMEOUT=30 ; fi
if [[ -z ${DIR_NAME} ]] ; then DIR_NAME=""

if [[ ! ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ! ${ENABLE_TIMEZONE_RANGE} == false ]] ; then ENABLE_TIMEZONE_RANGE=false ; fi
if [[ ! ${PERFORMANCE_TESTING} == true ]] && [[ ! ${PERFORMANCE_TESTING} == false ]] ; then PERFORMANCE_TESTING=false ; fi
if [[ ! ${COMPRESS} == true ]] && [[ ! ${COMPRESS} == false ]] ; then COMPRESS=false ; fi
if [[ ! ${EXCEPTION} == true ]] && [[ ! ${EXCEPTION} == false ]] ; then EXCEPTION=false ; fi


if [[ ! {INSERT_PROCESS} == file ]] || [[ ${COMPRESS} == false ]] ;
then
    if [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == false ]] && [[ ${EXCEPTION} == false ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME}
    elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == false ]] && [[ ${EXCEPTION} == false ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --enable-timezone-range
    elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == false ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --enable-timezone-range \
        --performance-testing
    elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == true ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --enable-timezone-range \
        --performance-testing \
        --exception
    elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == false ]] && [[ ${EXCEPTION} == true ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --enable-timezone-range \
        --exception
    elif [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == true ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --performance-testing \
        --exception
    elif [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == false ]] && [[ ${EXCEPTION} == true ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --exception
    fi
elif [[ {INSERT_PROCESS} == file ]] && [[ ${COMPRESS} == true ]];
then
    if [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == false ]] && [[ ${EXCEPTION} == false ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --compress
    elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == false ]] && [[ ${EXCEPTION} == false ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --compress \
        --enable-timezone-range
    elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == false ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --compress \
        --enable-timezone-range \
        --performance-testing
    elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == true ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --compress \
        --enable-timezone-range \
        --performance-testing \
        --exception
    elif [[ ${ENABLE_TIMEZONE_RANGE} == true ]] && [[ ${PERFORMANCE_TESTING} == false ]] && [[ ${EXCEPTION} == true ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --compress \
        --enable-timezone-range \
        --exception
    elif [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == true ]] && [[ ${EXCEPTION} == true ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --compress \
        --performance-testing \
        --exception
    elif [[ ${ENABLE_TIMEZONE_RANGE} == false ]] && [[ ${PERFORMANCE_TESTING} == false ]] && [[ ${EXCEPTION} == true ]] ;
    then
      python3.9 data_generator_generic.py ${DATA_TYPE} ${INSERT_PROCESS} ${DB_NAME} \
        --table-name ${TABLE_NAME} \
        --total-rows ${TOTAL_ROWS} \
        --sleep ${SLEEP} \
        --conn ${CONN} \
        --topic ${TOPIC} \
        --rest-timeout ${REST_TIMEOUT} \
        --dir-name ${DIR_NAME} \
        --compress \
        --exception
    fi
fi

