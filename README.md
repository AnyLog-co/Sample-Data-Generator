# Sample Data Generator
Sample data generators used to demonstrate and test AnyLog 

## Requirements 
```shell
python3 -m pip install -r $HOME/Sample-Data-Generator/requirements.txt
```

## Generic Data Generator 
[data_generator_generic.py](data_generator_generic_old.py) provides users different sets of dummy data, and send it into 
AnyLog via _MQTT_, _PUT_ or _POST_.

### Deployment
```shell
localhost:~/$ python3 Sample-Data-Generator/data_generator_generic.py --help
positional arguments:
  data_type   DATA_TYPE   type of data to insert into AnyLog  [default: trig]
      * trig
      * performance
      * ping
      * percentagecpu
      * opcua
      * power
      * examples - sample row(s) for each datta type
  insert_process    INSERT_PROCESS    format to store generated data    [default: print]
    * print
    * file
    * put
    * post
    * mqtt
  db_name   DB_NAME   logical database name     [default: test]
optional arguments:
  -h, --help            show this help message and exit
  --total-rows    TOTAL_ROWS      number of rows to insert. If set to 0, will run continuously    [default: 1000000]
  --batch-size    BATCH_SIZE      number of rows to insert per iteration                          [default: 1000]
  --sleep         SLEEP           wait time between each row                                      [default: 0.5]
  --timezone      TIMEZONE        timezone for generated timestamp(s)                             [default: utc | options: local,UTC,ET,BR,JP,WS,AU,IT]
  --enable-timezone-range     [ENABLE_TIMEZONE_RANGE]       set timestamp within a range of +/- 1 month
  --performance-testing       [PERFORMANCE_TESTING]         insert all rows within a 24 hour period
  --conn          CONN            {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
  --topic         TOPIC           topic for publishing data via REST POST or MQTT
  --rest-timeout  REST_TIMEOUT    how long to wait before stopping REST       [default: 30]
  --dir-name      DIR_NAME        directory when storing to file
  --compress      [COMPRESS]      whether to zip data dir
  --exception     [EXCEPTION]     whether to print exceptions


localhost:~/$ python3 Sample-Data-Generator/data_generator_generic.py trig post test \
  --total-rows 1000000 \
  --batch-size 1000 \
  --sleep 0.5 \
  --timezone local \
  --enable-timezone-range \
  --conn 10.0.0.226:32149 \
  --topic trig_data \
  --exception  

localhost:~/$ python3 Sample-Data-Generator/data_generator_generic.py performance mqtt test \
  --total-rows 1000000 \
  --batch-size 1000 \
  --sleep 0.5 \
  --timezone local \
  --performance-testing \ 
  --conn 10.0.0.226:32150 \
  --topic performance_data \
  --exception  
```

### Sample JSON
```json
# Data Type: trig
  {"dbms": "test", "table": "trig_data", "value": -3.141592653589793, "sin": -1.2246467991473532e-16, "cos": -1.0, "tan": 1.2246467991473532e-16, "timestamp": "2022-08-27T15:50:12.001399Z"}
        
# Data Type: performance
  {"dbms": "test", "table": "rand_data", "value": -1.2246467991473532e-16, "timestamp": "2022-08-27T15:50:12.163818Z"}
        
# Data Type: ping
  {"dbms": "test", "table": "ping_sensor", "device_name": "Ubiquiti OLT", "parentelement": "d515dccb-58be-11ea-b46d-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw", "value": 44.74, "timestamp": "2022-08-27T15:50:12.059726Z"}
        
# Data Type: percentagecpu
  {"dbms": "test", "table": "percentagecpu_sensor", "device_name": "VM Lit SL NMS", "parentelement": "1ab3b14e-93b1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H", "value": 9.59, "timestamp": "2022-08-27T15:50:12.116925Z"}
        
# Data Type: opcua
  {"dbms": "test2", "table": "opcua_readings", "fic1_pv": -103.29249139515318, "fic1_mv": -227.862187363, "fic1_sv": -48.493873977761645, "lic1_pv": 165.18648883311027, "lic1_mv": -84.59834643031611, "lic1_sv": 174.86936425992465, "fic2_pv": -37.52888216655371, "fic2_mv": 38.63696693385969, "fic2_sv": -182.07962937349504, "lic2_pv": 142.90402691921074, "lic2_mv": -35.64751556177472, "lic2_sv": -62.69296482664739, "fic3_pv": -147.060548270305, "fic3_mv": -57.93928389193016, "fic3_sv": 418.2631932904929, "lic3_pv": 176.7756420678825, "lic3_mv": -61.49695028678772, "lic3_sv": 220.60063882032966, "fic4_pv": -44.66240442407483, "fic4_mv": 11.529102739194443, "fic4_sv": 124.97175098185224, "lic4_pv": 9.507763915723592, "lic4_mv": 30.483647656168543, "lic4_sv": -213.4404433100362, "fic5_pv": -460.10226426203155, "fic5_mv": -72.96099747863087, "fic5_sv": -53.62672940378895, "lic5_pv": -89.93465024402398, "lic5_mv": -20.523831049180885, "lic5_sv": -125.29010564894106, "timestamp": "2022-09-24T14:30:10.575429Z"}
        
# Data Type: power
  {"dbms": "test", "table": "solar", "location": "38.89773, -77.03653", "value": 8.43453536493608, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "battery", "location": "38.89773, -77.03653", "value": 9.532695799656166, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "inverter", "location": "38.89773, -77.03653", "value": 20.03601934228979, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "eswitch", "location": "38.89773, -77.03653", "value": 9.530111494215165, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "pmu", "location": "38.89773, -77.03653", "value": 30.51712172789563, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "synchrophasor", "location": "38.89773, -77.03653", "phasor": "bXlvzdYc", "frequency": 1216.6996978149687, "dfreq": 2326.468559576384, "analog": 4.591088473171304, "timestamp": "2022-08-27T15:50:12.205323Z"}
```
## Video & Image Processing
[sample_data_generator_blobs.py](data_generator_blobs.py) stores images or videos into MongoDB, and associates them with
correlating data. The code requires using the images / videos found in our [Google Docs](https://drive.google.com/drive/folders/1sOYcH8Ie8tL4Cvt2xXEfLjlEz1yoYZMM?usp=sharing), 
which is open to the public. 


### AnyLog Requirements
Blobs data require: 
* [MongoDB](https://github.com/AnyLog-co/documentation/blob/mastaer/deployments/database_configuration.md#mongodb) to be 
running on the node - in order to accept blobs coming in
* `run mqtt client` active associated with the data coming 


### Deployment Options
```shell
localhost:~/$ python3 Sample-Data-Generator/data_generator_blobs.py --help 
positional arguments:
  dir_name              directory where files are stored - data is generated based on the file
  conn                  {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
  protocol              format to save data
    * post
    * mqtt
    * print      
optional arguments:
  -h, --help                show this help message and exit
  --topic       TOPIC       topic to send data agaisnt
  --db-name     DB_NAME     Logical database to store data in
  --table       TABLE       Logical database to store data in
  --sleep       SLEEP       Wait time between each file to insert
  --timeout     TIMEOUT     REST timeout (in seconds)
  --timezone    TIMEZONE    timezone for generated timestamp(s)
    * local 
    * utc 
    * et 
    * br
    * jp
    * ws
    * au
    * it
  --enable-timezone-range  [ENABLE_TIMEZONE_RANGE]   set timestamp within a range of +/- 1 month
  --reverse                [REVERSE]                 whether to store data in reversed (file) order
  --exception              [EXCEPTION]               whether to print exceptions to screen

localhost:~/$ python3 Sample-Data-Generator/data_generator_blobs.py $HOME/Downloads/sample_data/images 10.0.0.183:32149 post \
  --db-name test \
  --table factory_data \
  --topic image_mapping \
  --exception 
 
 localhost:~/$ python3 Sample-Data-Generator/data_generator_blobs.py $HOME/Downloads/sample_data/videos 10.0.0.183:32149 post \
  --db-name test \
  --table factory_data \
  --topic video-mapping \
  --sleep 10 \
  --reverse \
  --exception 
```

### Sample JSON
The first JSON object provides an example for video data. The video is associated with values, such as: 
* start / end timestamp 
* number of cars 
* speed 
While the second JSON provides an example of image data. The data is associated with information regarding the image,
such as:  
* whether it's _Ok_ or _Nok_ - `status`
* "coordinates" on the image that have a detected value - `detection`
```json
{
    "apiVersion": "v2",
    "id": "6b055b44-6eae-4f5d-b2fc-f9df19bf42cf",
    "deviceName": "anylog-data-generator",
    "origin": 1660163909,
    "profileName": "anylog-video-generator",
    "readings": [{
        "start_ts": "2022-01-01 00:00:00",
        "end_ts": "2022-01-01 00:00:05",
        "binaryValue": "AAAAHGZ0eXBtcDQyAAAAAWlzb21tcDQxbXA0MgADWChtb292AAAAbG12aGQAAAAA3xnEUt8ZxFMAAHUwAANvyQABAA",
        "mediaType": "video/mp4",
        "origin": 1660163909,
        "profileName": "traffic_data",
        "resourceName": "OnvifSnapshot",
        "valueType": "Binary",
        "num_cars": 5,
        "speed": 65.3
    }],
    "sourceName": "OnvifSnapshot"
}, 
{
    "id": "f85b2ddc-761d-88da-c524-12283fbb0f21",
    "dbms": "ntt",
    "table": "images",
    "file_name": "20200306202533614.jpeg",
    "file_type": "image/jpeg",
    "file_content": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD",
    "detection": [
            {"class": "kizu", "bbox": [666, 275, 682, 291], "score": 0.83249},
            {"class": "kizu", "bbox": [669, 262, 684, 277], "score": 0.83249},
            {"class": "kizu", "bbox": [688, 261, 706,276], "score": 0.72732},
            {"class": "kizu", "bbox": [698, 277, 713, 292], "score": 0.72659},
    ],
    "status": "ok"
}
```
