USER_INPUT=$1


if [[ ${USER_INPUT} == "query" ]] ; then
  curl -X GET 172.232.20.156:32349 \
    -H "command: sql new_company format=table and extend=(+node_name) and timezone=pt SELECT MIN(insert_timestamp), MAX(insert_timestamp), COUNT(*)::int::format(:,) FROM ping_sensor" \
    -H "User-Agent: AnyLog/1.23" \
    -H "destination: network"
  exit 1
fi

for CONN in 35.184.154.101 34.29.23.245 34.123.214.9 34.29.217.47 34.44.71.164 ; do
  if [[ ${USER_INPUT} == "clean" ]] ; then
    ssh -i ~/.ssh/gcloud moshe@${CONN} << EOF
      cd /home/moshe/docker-compose
      make clean ANYLOG_TYPE=operator
      export PGPASSWORD='demo'
      psql -h 127.0.0.1 -p 5432 -U admin -d postgres -c "DROP DATABASE IF EXISTS almgm;"
      psql -h 127.0.0.1 -p 5432 -U admin -d postgres -c "DROP DATABASE IF EXISTS new_company;"
EOF
  elif [[ ${USER_INPUT} == "up" ]] ; then
    ssh -i ~/.ssh/gcloud moshe@${CONN} << 'EOF'
      cd /home/moshe/docker-compose
      make up ANYLOG_TYPE=operator
EOF
  elif [[ ${USER_INPUT} == "log" ]] ; then
    curl -X GET ${CONN}:32149 -H "command: get processes"
EOF
  elif [[ ${USER_INPUT} == "summary" ]] ; then
    echo ${CONN}
#    curl -X GET ${CONN}:32149 -H "command: get streaming" -H "User-Agent: AnyLog/1.23"
    curl -X GET ${CONN}:32149 -H "command: get operator summary" -H "User-Agent: AnyLog/1.23"
EOF
  elif [[ ${USER_INPUT} == "reboot" ]] ; then
    ssh -i ~/.ssh/gcloud moshe@${CONN} << 'EOF'
      sudo reboot
EOF
  fi
done
