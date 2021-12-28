#!/bin/bash

error=0

if [[ ${HELP} == true ]] ; then python3 /app/Sample-Data-Generator/data_generator.py --help ; exit 1 ; fi

# validate base params
if [[ ${HELP} == true ]] ; then python3 data_generator.py --help ; exit 1 ; fi

if [[ ! ${CONN} ]] ; then echo Missing connection information ; error=1 ; fi
if [[ ! ${GENERATOR} ]] ; then echo Missing data generator information ; error=1 ; fi
if [[ ! ${SAVE} ]] ; then echo Missing format to save content as ; error=1 ; fi
if [[ ! ${DBMS} ]] ; then echo Missing logical database name ; error=1 ; fi

if [[ ${error} != 0 ]] ; then exit 1 ; fi

# Optional PARAMS
if [[ ${REPEAT} ]] ; then REPEAT=`echo --repeat ${REPEAT}` ; fi
if [[ ${SLEEP} ]] ; then SLEEP=`echo --sleep ${SLEEP}` ; fi
if [[ ${BATCH_REPEAT} ]] ; then BATCH_REPEAT=`echo --batch-repeat ${BATCH_REPEAT}` ; fi
if [[ ${BATCH_SLEEP} ]] ; then BATCH_SLEEP=`echo --batch-sleep ${BATCH_SLEEP}` ; fi
if [[ ${TIMEZONE} ]] ; then TIMEZONE=`echo --timezone ${TIMEZONE}`; fi
if [[ ${AUTHENTICATION} ]] ; then AUTHENTICATION=`echo --authentication ${AUTHENTICATION}` ; fi
if [[ ${TIMEOUT} ]] ; then TIMEOUT=`echo --timeout ${TIMEOUT}` ; fi
if [[ ${TOPIC} ]] ; then TOPIC=`echo --topic ${TOPIC}` ; fi
if [[ ${TOKEN} ]] ; then TOKEN=`echo --linode-token ${TOKEN}` ; fi
if [[ ${TAG} ]] ; then TAG=`echo --linode-tag ${TAG}` ; fi

if [[ ! ${EXCEPTION} == true ]] ; then
  python3 /app/Sample-Data-Generator/data_generator.py ${CONN} ${GENERATOR} ${SAVE} ${DBMS} ${REPEAT} ${SLEEP} ${BATCH_REPEAT} ${BATCH_SLEEP} ${TIMEZONE} ${AUTHENTICATION} ${TIMEOUT} ${TOPIC} ${TOKEN} ${TAG}
else
  python3 /app/Sample-Data-Generator/data_generator.py ${CONN} ${GENERATOR} ${SAVE} ${DBMS} ${REPEAT} ${SLEEP} ${BATCH_REPEAT} ${BATCH_SLEEP} ${TIMEZONE} ${AUTHENTICATION} ${TIMEOUT} ${TOPIC} ${TOKEN} ${TAG} -e
fi
