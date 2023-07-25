# Blobs
Sample data generator for blob data (ex. images and videos). Unlike non-blobs data, data can be inserted into AnyLog 
only via _MQTT_ or _REST POST_, and supports data coming in as [Base64](https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/), 
[OpemCV](https://www.geeksforgeeks.org/opencv-python-tutorial/) and [BytesIO](https://www.geeksforgeeks.org/python-bytes-method/) 

When using _MQTT_ or REST _POST_to insert data, users need to configure a [MQTT client](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#example)
* [EdgeX Data Generator (Base64)](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/demo_scripts/edgex_video_demo_base64.al)
* [Shared Video and Images (Base64)](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/demo_scripts/demo_video_images.al)
* [Generic Image processing](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/sample_code/blob_image_data.al)
* [Generic Video processing](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/sample_code/blob_video_data.al)


**Other Services**:
* [Generic Data Generator](README.md)

## Docker Deployment 
* Help 
```shell
# generic
docker run -it --detach-keys=ctrl-d --name data-generator --network host \
  -e HELP=true \
  --rm anylogco/sample-data-generator:latest
     
# generic help with detailed information such as sample call and aviloble data. 
docker run -it --detach-keys=ctrl-d --name data-generator --network host \
  -e EXTENDED_HELP=true \
  --rm anylogco/blobs-data-generator:latest
```
* EdgeX Data Generator
```shell
docker run -it --detach-keys=ctrl-d --name blobs-data-generator --network host \
  -e DATA_TYPE=edgex \
  -e INSERT_PROCESS=post \
  -e DB_NAME=test \
  -e TOTAL_ROWS=100 \
  -e BATCH_SIZE=10 \
  -e SLEEP=0.5 \
  -e CONN=198.74.50.131:32149,178.79.143.174:32149 \
  -e TIMEZONE=utc \
  -e TOPIC=anylogedgex-video-demo
  --rm anylogco/blobs-data-generator:latest
```

## Local Install
1. Clone Sample Data Generator
```shell
git clone https://github.com/AnyLog-co/Sample-Data-Generator
```

2. Install requirements - make sure python3 and python3-pip are installed   
```shell
python3 -m pip install -r $HOME/Sample-Data-Generator/requirements.txt
```

3. Run Data Generator
* Help
```shell
# generic
python3 Sample-Data-Generator/data_generator_generic_blobs.py
<< COMMENT
positional arguments:
  data_type             type of data to insert into AnyLog. Choices: edgex, video, image
  insert_process        format to store generated data. Choices: print, post, mqtt
  db_name               logical database name

optional arguments:
  -h, --help            show this help message and exit
  --extended-help [EXTENDED_HELP]
                        Generates help, but extends to include a sample row per data type
  --conversion-type CONVERSION_TYPE
                        Format to convert content to be stored in AnyLog. Choices: base64, bytesio, opencv
  --table-name TABLE_NAME
                        Change default table name
  --total-rows TOTAL_ROWS
                        number of rows to insert. If set to 0, will run continuously
  --batch-size BATCH_SIZE
                        number of rows to insert per iteration
  --sleep SLEEP         wait time between each row
  --timezone {local,utc,et,br,jp,ws,au,it}
                        timezone for generated timestamp(s)
  --enable-timezone-range [ENABLE_TIMEZONE_RANGE]
                        set timestamp within a range of +/- 1 month
  --conn CONN           {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
  --topic TOPIC         topic for publishing data via REST POST or MQTT
  --rest-timeout REST_TIMEOUT
                        how long to wait before stopping REST
  --qos {0,1,2}         MQTT Quality of Service
  --remote-data [REMOTE_DATA]
                        for images, use data from a remote source
  --url URL             URL for remote images
  --api-key API_KEY     API Key associated with remote images
  --authentication AUTHENTICATION
                        authentication key for URL
  --exception [EXCEPTION] whether to print exceptions
<<
python3 Sample-Data-Generator/data_generator_generic_blobs.py --extended-help
```
* edgex videos ins Base64 format
```shell
python3 Sample-Data-Generator/data_generator_generic_blobs.py edgex mqtt test \
  --total-rows 100 \
  --batch-size 10 \
  --sleep 30  \
  --conversion-type base64 \
  --conn 198.74.50.131:32150 \
  --timezone utc \
  --topic anylogedgex-video-demo
```
* Image in OpenCV format
```shell
python3 Sample-Data-Generator/data_generator_generic_blobs.py edgex post test \
  --total-rows 100 \
  --batch-size 10 \
  --sleep 30  \
  --conversion-type opencv \
  --conn 198.74.50.131:32149 \
  --timezone utc \
  --topic image-mapping
```

* Video in BytesIO format
```shell
python3 Sample-Data-Generator/data_generator_generic_blobs.py edgex post test \
  --total-rows 100 \
  --batch-size 10 \
  --sleep 30  \
  --conversion-type bytesio \
  --conn 198.74.50.131:32149 \
  --timezone utc \
  --topic video-mapping
```

## Sample JSON
```json
# Data Type: edgex
  {"dbms": "test", "table": "people_video", "start_ts": "2023-07-11T23:36:31.428555", "end_ts": "2023-07-11T23:36:36.428569", "file_content": "AAAAIGZ0eXBpc29tAAAC...", "count": 4, "confidence": 0.75}
# Data Type: image
  {"id": "57195181-21b1-4a1b-b21e-293783a267e4", "dbms": "test", "table": "images", "file_name": "20200306202534601.jpeg", "file_type": "image/jpeg", "file_content": "/9j/4AAQSkZJRgABAQAA...", "detection": [{"class": "kizu", "bbox": [658, 657, 674, 671], "score": 0.59605}], "status": "ok"}
# Data Type: video
  {"apiVersion": "v2", "dbName": "test", "id": "856e7dd0-ea63-4a8d-9f57-ba9f578c6fd2", "deviceName": "videos", "origin": 1689121459, "profileName": "anylog-video-generator", "readings": [{"timestamp": "2023-07-11T17:24:19.120476Z", "start_ts": "2023-07-11T17:24:19.120476Z", "end_ts": "2023-07-11T17:25:44.120476Z", "binaryValue": "AAAAIGZ0eXBpc29tAAAC...", "deviceName": "video18A", "id": "27618fc9-3df9-ee59-46e7-11748debdbe5", "mediaType": "video/mp4", "origin": 1689121459, "profileName": "mp4", "resourceName": "OnvifSnapshot", "valueType": "Binary", "num_cars": 40, "speed": 59.79}], "sourceName": "OnvifSnapshot"}
```