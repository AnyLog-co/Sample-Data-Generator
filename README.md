# Data Generator 
Python package providing an array of data types that can be sent to storage in the ways by which AnyLog supports. 
Ping and Percentage CPU data are based on data originally provided by a Fiber-optic comapny located in the Bay Area.

## Requirements 
For local install 
   * [psutil](https://pypi.org/project/psutil/)
   * [requests](https://pypi.org/project/requests/) 

Alternative users can run via [Docker](https://docs.docker.com/engine/install/) package

# How to Run 
## Python 
```
python3 data_generator.py  --help
   :positional arguments:
       dbms:str   - database name 
       sensor:str - type of sensor to get data from
         * machine          - boot time, cpu useage, swap memory percentage, disk useage percentege 
         * ping             - information regarding a ping sensor, data originally generated by Lite San Leandro devicies
         * percentagecpu    - information regarding a percentagecpu sensor, data originally generated by Lite San Leandro devicies
         * sin              - sin values over time 
         * cos              - cossin values over time      
         * rand             - random value generated 
   :optional arguments:
       -h, --help                          show this help message and exit
       -c, --conn         CONN             REST host and port                                                 (default: None)
       -f, --store-format STORE-FORMAT     format to get data                                                 (default: print)       {rest,file,print}
       -m, --mode         MODE             insert type                                                        (default: streamning)  {file,streaming}
       -i, --iteration    ITERATION        number of iterations. if set to 0 run continuesly                  (default: 1)
       -x, --frequency    FREQUENCY        value by which to multiply generated value(s)                      (default: 1)
       -r, --repeat       REPEAT           for machine & ping data number of rows to generate per iteration   (default: 10)
       -s, --sleep        SLEEP            wait between insert                                                (default: 0)
       -p, --prep-dir     PREP-DIR         directory to prepare data in                                       (default: $HOME/AnyLog-Network/data/prep)
       -w, --watch-dir    WATCH_DIR        directory for data ready to be stored                              (default: $HOME/AnyLog-Network/data/watch)
```

## Docker 
For Docker, a user is required to specify `dbms` and `sensor` enviorment variables. All others are optional, just like Python.  

```
docker run --name ${SENSOR}-data \
   -e dbms=${DATABASE_NAME} \ 
   -e sensor=${SENSOR} \ 
   -e conn=${CONN} \ 
   -e store_format=${STORE_FORMAT} \ 
   -e mode=${MODE} \
   -e iteration=${ITERATION} \ 
   -e frequency=${FREQUENCY} \ 
   -e repeat=${REPEAT} \ 
   -e sleep=${SLEEP} \ 
   -e prep_dir=${PREP-DIR} \ 
   -e watch_dir=${WATCH_DIR} \ 
   --network host anylogco/sample-data-generator
```

