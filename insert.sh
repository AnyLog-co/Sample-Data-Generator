for CONN in 35.184.154.101 34.29.23.245 34.123.214.9 34.29.217.47 34.44.71.164
do
{
    REST_CONN=$(curl -X GET "${CONN}:32149" \
      -H "command: blockchain get operator where ip=${CONN} bring [*][local_ip] : [*][rest_port]" \
      -H "User-Agent: AnyLog/1.23"
      )


    ssh -i ~/.ssh/gcloud moshe@${CONN} << EOF | grep -E "Benchmark started|Benchmark completed"
      echo ${REST_CONN}
      python3 ~/Sample-Data-Generator/benchmark_ping.py ping "${REST_CONN}" \
        --batch-size 5 \
        --total-rows 5 \
        --db-name new_company \
        --max-workers 1 \
        --sleep 0 \
        --single-insert \
        --exception

      python3 ~/Sample-Data-Generator/benchmark_ping.py ping "${REST_CONN}" \
        --batch-size 50000 \
        --total-rows 1000000 \
        --db-name new_company \
        --max-workers 1 \
        --sleep 0 \
        --single-insert \
        --exception

      python3 ~/Sample-Data-Generator/benchmark_ping.py ping "${REST_CONN}" \
        --batch-size 5 \
        --total-rows 5 \
        --db-name new_company \
        --max-workers 1 \
        --sleep 0 \
        --single-insert \
        --exception
EOF
} &
done
