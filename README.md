# Sample Data Generator

The _Sample Data Generator_ is used to insert data into AnyLog using REST (_PUT_ or _POST_), _MQTT_  and _Kafka_.

## Run
* Options
```text
positional arguments:
  data_generator    data to generate        {rand,ping,percentagecpu,cars,people,images}
  conn              connection information (example: [user]:[passwd]@[ip]:[port])
  publisher         format to publish data  {put,post,mqtt,kafka}
options:
  -h, --help                    show this help message and exit
  --batch-size  BATCH_SIZE      number of rows per insert batch                             [default: 10]
  --total-rows  TOTAL_ROWS      total rows to insert - if set to 0 then run continuously    [default: 10]
  --sleep       SLEEP           wait time between each row to insert                        [default: 0.5]
  --db-name     DB_NAME         logical database name                                       [default: test]
  --topic       TOPIC           topic name for POST, MQTT and Kafka                         [default: anylog-demo]
  --timeout     TIMEOUT         REST timeout                                                [default: 30]
  --qos         QOS             Quality of Service      {0,1,2,3}                           [default: 0] 
  --exception   [EXCEPTION]     Whether to print exceptions                                 [default: false]
  --examples    [EXAMPLES]      print example calls and sample data                         [default: false] 
```

* Sample REST _PUT_
```shell
docker run --network host \
  -e DATA_GENERATOR=rand \
  -e CONN=127.0.0.1:32149
  -e PUBLISHER=put \
  -e DB_NAME=test \
  -e TIMEEOUT 30 \
--rm anylogco/sample-data-generator:latest  
```

* Sample _Kafka_
```shell
docker run --network host \
  -e DATA_GENERATOR=rand \
  -e CONN=35.188.2.231:1883 \
  -e PUBLISHER=kafka \
  -e DB_NAME=test \
  -e TOPIC=anylog-demo
--rm anylogco/sample-data-generator:latest  
```

* Sample _MQTT_ 
```shell
docker run --network host \
  -e DATA_GENERATOR=rand \
  -e CONN=anyloguser:mqtt4AnyLog!@35.188.2.231:9092 \
  -e PUBLISHER=mqtt \
  -e DB_NAME=test \
  -e TOPIC=anylog-demo
--rm anylogco/sample-data-generator:latest
```

## Sample Data 
* [random value](data_generator/rand_data.py) - Random value
```json
{
  "dbms": "test", 
  "table": "rand_data", 
  "timestamp": "2024-03-22T02:45:19.923966Z", 
  "value": 41.243
}
```

* [Ping / PercentageCPU](data_generator/ping_percentagecpu.py) - Data for networking equipment and switches
```json
{
  "dbms": "test", 
  "table": "ping_sensor", 
  "timestamp": "2024-03-22T02:45:19.925005Z", 
  "device_name": "Catalyst 3500XL", 
  "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba", 
  "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", 
  "value": 21.11
}
{
  "dbms": "test", 
  "table": "percentagecpu_sensor", 
  "timestamp": "2024-03-22T02:45:19.925054Z", 
  "device_name": "ADVA FSP3000R7", 
  "parentelement": "62e71893-92e0-11e9-b465-d4856454f4ba", 
  "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H",
  "value": 4.51
}
```

* [Images](data_generator/blobs_factory_images.py) - Factory images analysis

<img src="blobs/factory_images/20200306202533614.jpeg" width="40%" height="40%" />

* [People Counter](data_generator/blob_people_video.py) - AI to count number of people in a video

* [Car Counter](data_generator/blobs_car_video.py) - using _Tensorflow_, calculate number of cars in a video
