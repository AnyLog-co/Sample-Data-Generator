# Data Generator

This repository provides a data generator that can simulate and insert data into an OPC-UA server or a database. It is 
configurable through command-line arguments and environment variables. This generator supports multiple data types and 
publishing methods, including PUT, POST, MQTT, and Kafka. Additionally, it supports OPC-UA server configuration and 
connection details for data generation.

## Setup

To set up and use the sample data generator, you can either run it directly from the source code or pre-built Docker 
container. This generator can simulate data for both OPC-UA servers and database connections, providing flexibility in 
use cases.

If you're running the script directly from the repository, ensure you have Python installed along with the required 
libraries. Install the necessary Python packages:
```bash
pip install -r requirements.txt
```

If you're running the script via Docker, ensure you have docker installed: 
```shell
sudo snap install docker
sudo apt-get -y install docker-compose 
sudo apt-get -y install make
 
# Grant non-root user permissions to use docker
USER=`whoami`
sudo groupadd docker 
sudo usermod -aG docker ${USER} 
newgrp docker
```


## Command Line Arguments
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Command-Line Arguments</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        caption {
            font-size: 1.5em;
            margin: 10px;
        }
    </style>
</head>
<body>

<h1>Command-Line Arguments</h1>

<!-- Data Generator Table -->
### Data Generator Parameters
<table>
    <caption>Positional Arguments</caption>
    <thead>
        <tr>
            <th>ENV var</th>
            <th>Python3 Param</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>DATA_GENERATOR</td>
            <td>data_generator</td>
            <td>Type of data generator to use (e.g., 'rand', 'seq', etc.; default: 'rand')</td>
        </tr>
        <tr>
            <td>CONN</td>
            <td>conn</td>
            <td>Connection string in the format [user]:[password]@[ip]:[port] (default: '127.0.0.1:32149')</td>
        </tr>
        <tr>
            <td>PUBLISHER</td>
            <td>publisher</td>
            <td>Format to publish data (choices: 'put', 'post', 'mqtt', 'kafka'; default: 'put')</td>
        </tr>
    </tbody>
</table>

<table>
    <caption>Optional Arguments</caption>
    <thead>
        <tr>
            <th>ENV var</th>
            <th>Python3 Param</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>BATCH_SIZE</td>
            <td>--batch-size</td>
            <td>Number of rows per insert batch (default: 10)</td>
        </tr>
        <tr>
            <td>TOTAL_ROWS</td>
            <td>--total-rows</td>
            <td>Total rows to insert. If 0, runs continuously (default: 10)</td>
        </tr>
        <tr>
            <td>SLEEP</td>
            <td>--sleep</td>
            <td>Wait time between each row insertion (default: 0.5)</td>
        </tr>
        <tr>
            <td>DB_NAME</td>
            <td>--db-name</td>
            <td>Logical database name (default: 'test')</td>
        </tr>
        <tr>
            <td>TOPIC</td>
            <td>--topic</td>
            <td>Topic name for POST, MQTT, and Kafka (default: 'anylog-demo')</td>
        </tr>
        <tr>
            <td>TIMEOUT</td>
            <td>--timeout</td>
            <td>REST timeout in seconds (default: 30)</td>
        </tr>
        <tr>
            <td>QOS</td>
            <td>--qos</td>
            <td>Quality of Service (default: 0; options: 0-3)</td>
        </tr>
        <tr>
            <td>EXCEPTION</td>
            <td>--exception</td>
            <td>Whether to print exceptions (default: False)</td>
        </tr>
        <tr>
            <td>IS_AGGREGATED</td>
            <td>--is-aggregated</td>
            <td>Allow static values for aggregated data (default: False)</td>
        </tr>
        <tr>
            <td>TOLERANCE_LEVEL</td>
            <td>--tolerance-level</td>
            <td>Accepted tolerance level for aggregated values (default: 0)</td>
        </tr>
        <tr>
            <td>EXAMPLES</td>
            <td>--examples</td>
            <td>Print example calls and sample data (default: False)</td>
        </tr>
    </tbody>
</table>

</body>
</html>

<!-- OPC-UA Table -->
### OPCUA Params 
<table>
    <caption>Positional Arguments</caption>
    <thead>
        <tr>
            <th>ENV var</th>
            <th>Python3 Param</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>IP</td>
            <td>ip</td>
            <td>IP address of the OPC-UA server (default: '0.0.0.0')</td>
        </tr>
        <tr>
            <td>PORT</td>
            <td>port</td>
            <td>Port number of the OPC-UA server (default: 4840)</td>
        </tr>
    </tbody>
</table>

<table>
    <caption>Optional Arguments</caption>
    <thead>
        <tr>
            <th>ENV var</th>
            <th>Python3 Param</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>SLEEP</td>
            <td>--sleep</td>
            <td>Time in seconds between operations (default: 2)</td>
        </tr>
        <tr>
            <td>DB_NAME</td>
            <td>--db-name</td>
            <td>Logical database name (default: 'test')</td>
        </tr>
        <tr>
            <td>CREATE_DATA_SIZE</td>
            <td>--create-data-size</td>
            <td>Create a larger data set for testing (default: False)</td>
        </tr>
        <tr>
            <td>NUM_TABLES</td>
            <td>--num-tables</td>
            <td>Number of tables for large data sets (default: 20)</td>
        </tr>
        <tr>
            <td>NUM_COLUMNS</td>
            <td>--num-columns</td>
            <td>Number of columns per table (default: 100)</td>
        </tr>
        <tr>
            <td>SHOW_QUALITY</td>
            <td>--show-quality</td>
            <td>Display quality for numeric columns (default: False)</td>
        </tr>
    </tbody>
</table>






## Sample Data & Calls 
### Sample Calls 
When sending data via REST POST, MQTT or Kafka, make sure there's a message client accept the data
* Run Data Generator with Default Values
```shell
docker run --rm \
  -e DATA_GENERATOR=r_50 \
  -e CONN=127.0.0.1:32149 \
  -e PUBLISHER=put \
  -e BATCH_SIZE=10 \
  -e TOTAL_ROWS=10 \
  -e SLEEP=0.5 \
  -e DB_NAME=test \
  -e TOPIC=anylog-demo \
  -e TIMEOUT=30 \
  -e QOS=0 \
  -e EXCEPTION=false \
  -e IS_AGGREGATED=false \
  -e TOLERANCE_LEVEL=0 \
  -e EXAMPLES=false \
  anylogco/sample-data-generator
```
* Run with MQTT
```shell
docker run --rm \
  -e DATA_GENERATOR=ping \
  -e CONN=127.0.0.1:32150 \
  -e PUBLISHER=mqtt \
  -e BATCH_SIZE=10 \
  -e TOTAL_ROWS=10 \
  -e SLEEP=0.5 \
  -e DB_NAME=test \
  -e TOPIC=anylog-demo \
  -e TIMEOUT=30 \
  -e QOS=0 \
  -e EXCEPTION=false \
  -e IS_AGGREGATED=false \
  -e TOLERANCE_LEVEL=0 \
  -e EXAMPLES=false \
  anylogco/sample-data-generator
```

* Run the Data Generator with Sequence Data or Aggregated data
```shell
docker run --rm \
  -e DATA_GENERATOR=rand \
  -e CONN=127.0.0.1:32149 \
  -e PUBLISHER=mqtt \
  -e BATCH_SIZE=10 \
  -e TOTAL_ROWS=100 \
  -e SLEEP=0.5 \
  -e DB_NAME=test \
  -e TOPIC=anylog-demo \
  -e TIMEOUT=30 \
  -e QOS=0 \
  -e EXCEPTION=false \
  -e IS_AGGREGATED=true \
  -e TOLERANCE_LEVEL=5 \ # 0.05 difference in value  
  -e EXAMPLES=false \
  anylogco/sample-data-generator
```

* Send data via OPC-UA
```shell
docker run --rm \
  -e ENV_RUN_OPCUA=true \
  -e IP=192.168.1.100 \
  -e PORT=4880 \
  -e SLEEP=2 \
  -e DB_NAME=test \
  anylogco/sample-data-generator
```

### Sample Data 
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