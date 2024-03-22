# Sample Data Generator

The _Sample Data Generator_ is used to insert data into AnyLog using REST (_PUT_ or _POST_), _MQTT_  and _Kafka_.

## Run


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

<img src="blobs/people_video/edgex4.mp4#t=1" width="40%" height="40%" />

* [Car Counter](data_generator/blobs_car_video.py) - using _Tensorflow_, calculate number of cars in a video

<img src="blobs/car_video/video1A.mp4#t=1" width="40%" height="40%" />
