#!/bin/bash

if [[ ${INSERT_PROCESS} -eq print ]]
then
  bash ${ANYLOG_PATH}/bash_scripts/print_data.sh
elif [[ ${INSERT_PROCESS} -eq file ]]
then
  bash ${ANYLOG_PATH}/bash_scriprts/file_data.sh
elif [[ ${INSERT_PROCESS} -eq put ]]
then
  bash ${ANYLOG_PATH}/bash_scripts/rest_put_data.sh
elif [[ ${INSERT_PROCESS} -eq post ]]
then
  bash ${ANYLOG_PATH}/bash_scripts/rest_post_data.sh
elif [[ ${INSERT_PROCESS} -eq mqtt ]]
then
  bash ${ANYLOG_PATH}/bash_scripts/rest_matt_data.sh
fi

