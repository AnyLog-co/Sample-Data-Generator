# The following allows for a Docker deployment of AnyLog's data generator 
#    :positional arguments:
#        dbms       database name
#        sensor     type of sensor to get data from    {machine,percentagecpu,ping,sin,cos,rand}
#    :optional arguments:
#        -h,  --help             show this help message and exit
#        -c,  --conn             REST host and port                                                    (default: '')
#        -f,  --store-format     format to get data                                                    (default: print)        {rest,file,print}
#        -m,  --mode             insert type                                                           (default: streaming)    {file,streaming}
#        -i,  --iteration        number of iterations. if set to 0 run continuesly                     (default: 1)
#        -r,  --repeat           For machine & ping data number of rows to generate per iteration      (default: 10)
#        -s,  --sleep            wait between insert                                                   (default: 0)
#        -p,  --prep-dir         directory to prepare data in                                          (default: $HOME/AnyLog-Network/data/prep)
#        -w,  --watch-dir        directory for data ready to be stored                                 (default: $HOME/AnyLog-Network/data/watch)
#        -mc, --mqtt-conn        MQTT connection info                                                  (default: mqwdtklv@driver.cloudmqtt.com:uRimssLO4dIo)
#        -mp, --mqtt-port        MQTT port  	 		       			               (default: 18975)
#        -mt, --mqtt-topic       MQTT topic 							       (default: test)
 
# Get help 
if [[ ${HELP} == true ]] 
then 
    python3 /app/Sample-Data-Generator/data_generator.py --help 
    exit 1 
fi 

# Validate dbms & sensor are set 
ERROR='' 
STATUS=0 

if [[ -z ${DBMS} ]] 
then 
    ERROR="dbms cannot be empty" 
    STATUS=1 
fi 
if [[ -z ${SENSOR} ]] && [[ ${STATUS} -eq 1 ]] 
then
    ERROR="${error} & sensor cannot be empty\nsensor options:\n\tmachine\n\tpercentagecpu\n\tping\n\tcos\n\tsin\n\trand\n" 
    STATUS=2
elif [[ -z ${STATUS} ]]
then 
    ERROR="sensor cannot be empty\nsensor options:\n\tmachine\n\tpercentagecpu\n\tping\n\tcos\n\tsin\n\trand\n" 
    STATUS=1 
fi 

if [[ ${STATUS} -gt 0 ]] 
then 
    printf "${ERROR}" 
    exit 1 
fi 


# configure optional arguments, if empty 
if [[ -z ${STORE_FORMAT} ]] ; then STORE_FORMAT='print' ; fi 
if [[ -z ${MODE}         ]] ; then MODE='streaming'     ; fi 
if [[ -z ${ITERATION}    ]] ; then ITERATION=1          ; fi 
if [[ -z ${FREQUENCY}    ]] ; then FREQUENCY=1          ; fi 
if [[ -z ${REPEAT}       ]] ; then REPEAT=10            ; fi 
if [[ -z ${SLEEP}        ]] ; then SLEEP=0              ; fi 
PARAMS="--store-format ${STORE_FORMAT} --mode ${MODE} --iteration ${ITERATION} --frequency ${FREQUENCY} --repeat ${REPEAT} --sleep ${SLEEP} "

if [[ ${STORE_FROMAT} == "file" ]] 
then 
    if [[ -z ${PREP_DIR}  ]] ; then PREP_DIR='/app/AnyLog-Network/data/prep_dir' ; fi 
    if [[ -z ${WATCH_DIR} ]] ; then WATCH_DIR='/app/AnyLog-Network/data/watch_dir' ; fi 
    PARAMS="${PARAMS} --prep-dir ${PREP_DIR} --watch-dir ${WATCH_DIR}" 
elif [[ ${STORE_FORMAT} == "rest" ]] || [[ ${STORE_FORMAT} == "rest_mqtt" ]]  
then 
    if [[ -z ${CONN} ]] ; then CONN=None ; fi 
    PARAMS="${PARAMS} --conn ${CONN}" 
elif [[ ${STORE_FORMAT} == "rest_mqtt" ]] || [[ ${STORE_FORMAT} == "mqtt" ]]  
then 
    if [[ -z ${MQTT_CONN}      ]] ; then MQTT_CONN='mqwdtklv@driver.cloudmqtt.com:uRimssLO4dIo'   ; fi 
    if [[ -z ${MQTT_PORT}      ]] ; then MQTT_PORT=18975         				  ; fi 
    if [[ -z ${MQTT_TOPIC}     ]] ; then MQTT_TOPIC='test'       				  ; fi  
    #if [[ -z {QUALITY_SERVICE} ]] ; then QUALITY_SERVICE=0                                        ; fi 
    PARAMS="${PARAMS} --mqtt-conn ${MQTT_CONN} --mqtt-port ${MQTT_PORT} --mqtt-topic ${MQTT_TOPIC}"
fi 
#echo "python3 Sample-Data-Generator/data_generator.py ${DBMS} ${SENSOR} ${PARAMS}"
python3 Sample-Data-Generator/data_generator.py ${DBMS} ${SENSOR} ${PARAMS}

