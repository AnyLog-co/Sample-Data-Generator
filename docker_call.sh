#!/bin/bash

if [[ ${INSERT_PROCESS} == print ]] ;
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/print_data.sh
elif [[ ${INSERT_PROCESS} == file ]] ;
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/store_data_file.sh
elif [[ ${INSERT_PROCESS} == put ]] ;
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/send_put_data.sh
elif [[ ${INSERT_PROCESS} == post ]] ;
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/send_post_data.sh
elif [[ ${INSERT_PROCESS} == mqtt ]] ;
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/send_mqtt_data.sh
elif [[ ${INSERT_PROCESS} == help ]] ;
then
  python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py --help
  python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py examples print test
fi
