#k6 run --env VUS=1 \
#        --env URL=35.184.154.101:32149 \
#        --env BATCH_SIZE=5 \
#        --env SLEEP=0 \
#        --env ITERATIONS=1 \
#        --env NODE_ID_LENGTH=10 \
#        --env SINGLE_INSERT=true \
#        --env TIMEOUT=120 \
#        --env EXCEPTION=true \
#        ~/Sample-Data-Generator/k6/script.js

#sleep 10

k6 run --env VUS=1 \
        --env URL=35.184.154.101:32149 \
        --env BATCH_SIZE=10000 \
        --env SLEEP=0 \
        --env ITERATIONS=100 \
        --env NODE_ID_LENGTH=10 \
        --env SINGLE_INSERT=true \
        --env TIMEOUT=120 \
        --env EXCEPTION=true \
        ~/Sample-Data-Generator/k6/script.js

#read -p "Continue "
#
#k6 run --env VUS=1 \
#        --env URL=35.184.154.101:32149 \
#        --env BATCH_SIZE=5 \
#        --env SLEEP=0 \
#        --env ITERATIONS=1 \
#        --env NODE_ID_LENGTH=10 \
#        --env SINGLE_INSERT=true \
#        --env TIMEOUT=120 \
#        --env EXCEPTION=true \
#        ~/Sample-Data-Generator/k6/script.js
