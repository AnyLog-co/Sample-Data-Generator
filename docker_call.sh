#!/bin/bash

if [[ ${HELP} -eq true ]]
then
  python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py --help
  printf "\nSample Data Types & Corresponding Values\n"
  python3.9 ${ANYLOG_PATH}/Sample-Data-Generator/data_generator.py examples print test
elif [[ ${INSERT_PROCESS} -eq print ]]
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/print_data.sh
elif [[ ${INSERT_PROCESS} -eq file ]]
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scriprts/store_data_file.sh
elif [[ ${INSERT_PROCESS} -eq put ]]
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/rest_put_data.sh
elif [[ ${INSERT_PROCESS} -eq post ]]
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/rest_post_data.sh
elif [[ ${INSERT_PROCESS} -eq mqtt ]]
then
  bash ${ANYLOG_PATH}/Sample-Data-Generator/bash_scripts/send_mqtt_data.sh
fi

