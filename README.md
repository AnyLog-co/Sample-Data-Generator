# Sample Data Generator

The following provides an array of data sets to be stored into AnyLog/EdgeLake via _REST_ (PUT and POST), _MQTT_ and 
_Kafka_. 

### Requirements
* Docker

<div align="center"><b>- OR -</b></div>

* Python>=3.9 with the following [requirements](requirements.txt)
  * Flask==2.2.2 
  * tensorflow==2.11.0 
  * numpy==1.23.5 
  * opencv-python-headless==4.6.0.66 
  * requests==2.28.1 
  * kafka-python==2.0.2 
  * paho-mqtt==1.6.1 
  * concurrent.futures==3.1.1
  * pyyaml==6.0 
  * pandas==1.5.2
  * opcua>=0.0

### Options
```README.md
:positional arguments:
    data_type       data to generate
    - ping
    - percentagecpu
    - rand
    - r_50
    - large
    - car
    - people
    - factory
    publisher       format to publish data
    - put
    - post
    - mqtt
    - kafka
    - server
    - opcua
    db_name         logical database name
:optional arguments:
    -h, --help                      show this help message and exit
    --rest-conn     REST_CONN       connection information used for PUT, POST, MQTT and Kafka (example: [user]:[passwd]@[ip]:[port])
    --batch-size    BATCH_SIZE      number of rows per insert batch
    --total-rows    TOTAL_ROWS      total rows to insert - if set to 0 then run continuously
    --sleep         SLEEP           wait time between each row to insert
    --topic         TOPIC           topic name for POST, MQTT and Kafka
    --timeout       TIMEOUT         REST timeout
    --qos           {0,1,2,3}       Quality of Service
    --service-port  SERVICE_PORT    Server or OPC-UA service port
    --create-large-data     [CREATE_LARGE_DATA]     Create new data set for large data
    --num-tables            NUM_TABLES              when creating a large data set, number of tables
    --num-columns           NUM_COLUMNS             number of columns per
    --exception             [EXCEPTION]             Whether to print exceptions
```

### Sample Calls

* view help
```shell
docker run -it -e VIEW_HELP=true --rm anylogco/sample-data-generator:latest 
```

* Server
  * large data - http://127.0.0.1:8481//simulated_data/large
  * ping - http://127.0.0.1:8481//simulated_data/ping
  * percentagecpu - http://127.0.0.1:8481//simulated_data/percentagecpu
  * random - http://127.0.0.1:8481//simulated_data/rand
  * r_50 - http://127.0.0.1:8481//simulated_data/r_50
```shell
docker run -it \
  -p 8481:8481 \
  -e PUBLISHER=server \
  -e SERVICE_PORT=8481 \
--rm anylogco/sample-data-generator:latest
```
<img src="sample_server.png" height="75%" width="75%" align="center" />

* OPC-UA 
```shell
docker run -it \
  -p 4840:4840 \
  -e PUBLISHER=opcua \
  -e SERVICE_PORT=4840 \
--rm anylogco/sample-data-generator:latest
```
**Process**: under _large_ namespace the number of tables (`ns=2;i=X`) depends on [opcua_describe_data.json](blobs/opcua_describe_data.json).
While under _network_ there's both _ping_ and _percentagecpu_ data.  
```anylog
# view list of namespaces
AL anylog-node +> get opcua namespace where  url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator 

OPCUA Namespace Table
Index Namespace URL                
-----|----------------------------|
    0|http://opcfoundation.org/UA/|
    1|urn:freeopcua:python:server |
    2|large                       |
    3|network                     |
    4|rand                        |
    5|r_50                        |


# view columns / tables in a givenn namespace
AL anylog-node +> get opcua struct where  url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and node="ns=2;i=2"

[object], (ns=2;n=2, name=table_2, datatype=None)
  [variable], (ns=2;s=table_2_timestamp, name=timestamp, datatype=VariantType.String)
  [variable], (ns=2;s=table_2_device_id, name=device_id, datatype=VariantType.String)
  [variable], (ns=2;s=table_2_column_1, name=column_1, datatype=VariantType.Int64)
  [variable], (ns=2;s=table_2_column_2, name=column_2, datatype=VariantType.Boolean)
  [variable], (ns=2;s=table_2_column_3, name=column_3, datatype=VariantType.Double)
  [variable], (ns=2;s=table_2_column_4, name=column_4, datatype=VariantType.Null)
  [variable], (ns=2;s=table_2_column_5, name=column_5, datatype=VariantType.Int64)

# Generate get values command for ns=2;i=1
AL anylog-node +> <get opcua struct where 
  url=opc.tcp://127.0.0.1:4840/freeopcua/data-generator and 
  node="ns=2;i=1" and 
  class = variable and
  format = get_value and 
  validate=true>


Processing nodes #0 - #999  [                                                  ]

AL anylog-node +> 

<get opcua values where url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and nodes = ["ns=2;s=table_1_timestamp","ns=2;s=table_1_device_id","ns=2;s=table_1_column_1","ns=2;s=table_1_column_2","ns=2;s=table_1_column_3"
,"ns=2;s=table_1_column_4","ns=2;s=table_1_column_5"]> 

# View data
AL anylog-node +> <get opcua values where url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and nodes = ["ns=2;s=table_1_timestamp","ns=2;s=table_1_device_id","ns=2;s=table_1_column_1","ns=2;s=table_1_column_2","ns=2;s=table_1_column_3"
,"ns=2;s=table_1_column_4","ns=2;s=table_1_column_5"] and include=all>

OPCUA Nodes values
id                       name      source_timestamp           server_timestamp status_code value                                
------------------------|---------|--------------------------|----------------|-----------|------------------------------------|
ns=2;s=table_1_timestamp|timestamp|2025-01-17 21:22:56.636516|                |Good       |2025-01-17T13:22:56.635006Z         |
ns=2;s=table_1_device_id|device_id|2025-01-17 21:22:56.636677|                |Good       |fc2fea9a-a85a-4457-8e8b-e9c0b7adc4fe|
ns=2;s=table_1_column_1 |column_1 |2025-01-17 21:22:56.636805|                |Good       |False                               |
ns=2;s=table_1_column_2 |column_2 |2025-01-17 21:22:56.636922|                |Good       |                             312.253|
ns=2;s=table_1_column_3 |column_3 |2025-01-17 21:22:56.637041|                |Good       |                             486.845|
ns=2;s=table_1_column_4 |column_4 |2025-01-17 21:22:56.637156|                |Good       |                             225.557|
ns=2;s=table_1_column_5 |column_5 |2025-01-17 21:22:56.637271|                |Good       |VcQBCVzPE                           |
```

* PUT 
```shell
docker run -it -d \
  -e DATA_TYPE=ping \
  -e PUBLISHER=put \
  -e DB_NAME=test \
  -e REST_CONN=127.0.0.1:32149 \
  -e BATCH_SIZE=10 \
  -e TOTAL_ROWS=100 \
  -e SLEEP=0.5 \
  -e TIMEOUT=30 \
--network host --rm anylogco/sample-data-generator:latest
```

* POST 
```shell
docker run -it -d \
  -e DATA_TYPE=people \
  -e PUBLISHER=post \
  -e DB_NAME=test \
  -e REST_CONN=127.0.0.1:32149 \
  -e BATCH_SIZE=10 \
  -e TOTAL_ROWS=100 \
  -e SLEEP=0.5 \
  -e TIMEOUT=30 \
  -e TOPIC=people-imgs \
--network host --rm anylogco/sample-data-generator:latest
```

* MQTT
```shell
docker run -it -d \
  -e DATA_TYPE=r_50 \
  -e PUBLISHER=mqtt \
  -e DB_NAME=test \
  -e REST_CONN=127.0.0.1:32150 \
  -e BATCH_SIZE=10 \
  -e TOTAL_ROWS=100 \
  -e SLEEP=0.5 \
  -e QOS=1 \
  -e TOPIC=machine-data \
--network host --rm anylogco/sample-data-generator:latest
```

* Kafka
```shell
docker run -it -d \
  -e DATA_TYPE=large \
  -e PUBLISHER=kafka \
  -e DB_NAME=test \
  -e REST_CONN=127.0.0.1:32150 \
  -e BATCH_SIZE=10 \
  -e TOTAL_ROWS=100 \
  -e SLEEP=0.5 \
  -e QOS=1 \
  -e TOPIC=large-data \
  -e CREATE_LARGE_DATA=true \
  -e NUM_TABLES=10 \
  -e NUM_COLUMNS=10 \
  -v /app/Sample-Data-Generator/blobs:blob-data
--network host --rm anylogco/sample-data-generator:latest
```

**Notes and comments**: 
* When sending data via _POST_, _MQTT_ or _Kafka_ make sure a message client is active to accept the data
into AnyLog/EdgeLake

* Description for large data can be found [opcua_describe_data.json](blobs/opcua_describe_data.json). When running with 
_large_ data_type, we recommend to make blobs persistent (Kafka option provides an example) and remove `CREATE_LARGE_DATA`
after the first run for data consistency.