#!/bin/bash

#---------------------------------------------------------------------------------------#
# send data to node - the first time last 15 minutes, then every 90 seconds (with sleep)
#---------------------------------------------------------------------------------------#

CONN_IP=$1
CONN_PORT=$2

NOW=`date -d "$current_date - 15 minutes" '+%Y-%m-%d %H:%M:%S.%6N'`
while : ; do
   journalctl --since "${NOW}" | awk '{print "al.sl.header.new_company.syslog", $0}' | nc -w 1 ${CONN_IP} ${CONN_PORT}
   sleep 90
   NOW=`date -d "$current_date - 90 secnds" '+%Y-%m-%d %H:%M:%S.%6N'`
done
