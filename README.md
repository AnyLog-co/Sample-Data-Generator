# Sample Data Generator
The following repository is a tool allowing to easily send data into AnyLog using different protocols

### Types of Data Generated
* [Linode](data_generators/linode.py) - Using the [Linode API](https://www.linode.com/docs/api) get information regarding
`CPU`, `IO` and `network` statistics. 
* [Traffic Data](data_generators/traffic_data.py) - Using the [TomTom API](https://developer.tomtom.com/products/traffic-api) 
get insight regarding traffic information for a subset of key intersections in the Bay Area. 
* [EdgeX Data](data_generators/edgex_rest.py) - Extract data from local [EdgeX](https://www.edgexfoundry.org/get-started/) 
instance via REST
* [Read File](data_generators/read_file.py) - Read content from file 
* [Trig](data_generators/trig.py) - Generate `sin` and `cos` graph values 
* Customer based data sets
  * [Ping Sensor](data_generators/ping_sensor.py) & [Percentage CPU Sensor](data_generators/percentagecpu_sensor.py) - 
  sample ping and percentage cpu information for different types of switches
  * [Power Company](data_generators/power_company.py) & [Synchrophizer](data_generators/power_company_synchrophasor.py) - 
  Sample insight for things that are of interest to a customer dealing with power utilization
  * [OPCUA Data](data_generators/opcua_data.py) - Sample data set for a subset of OPCUA devices provided by a customer

### Supported Protocols 
In addition to an array of data sets that can be generated the data generator provides an array of options for sending data
* [file](protocols/generic_protocol.py) - Generated data would be stored to file 
* [print](protocols/generic_protocol.py) - Generated data would be printed on the screen
* [MQTT](protocols/generic_protocol.py) - Send data via MQTT, either using AnyLog as a publisher, or a built-in process that uses
_python_ to publish the data into a broker
* [Kafka](protocols/kafka_protocol.py) - Send data into a Kafka broker 
* [REST](protocols/rest.py) - Send data using either _PUT_ or _POST_ 

## Deployment
### Requirements
* gzip 
* [kafka](https://pypi.org/project/kafka/)
* [paho.mqtt](https://pypi.org/project/paho-mqtt/)
* [pytz](https://pypi.org/project/pytz/)
* [tzlocal](https://pypi.org/project/tzlocal/)

### Options 
```
:positional arguments:
    conn                    IP:Port credentials for either REST, MQTT or Kafka
    data-generator          data set to generate content for                    
        --> file
        --> linode
        --> percentagecpu
        --> ping
        --> edgex
        --> power
        --> synchrophasor
        --> trig (default)
        --> opcua
        --> traffic
    protocol                format to save data                                                     
        --> put 
        --> post
        --> mqtt 
        --> kafka
        --> file 
        --> print (default)
    dbms                    Logical database to store data in
:optional arguments:
  -h, --help            show this help message and exit
  --repeat              number of time to repeat each batch, if 0 then run continuously
  --sleep               sleep time between each batch
  --batch-repeat        number of rows per batch
  --batch-sleep         sleep time between rows or a specific batch
  --timezone            timezone for generated timestamp(s)
    --> local
    --> UTC
    --> ET
    --> BR
    --> JP
    --> WS
    --> AU
    --> IT
  --enable-timezone-range   whether or not to set timestamp within a "range"
  --authentication          username, password
  --timeout                 REST timeout (in seconds)
  --topic                   topic for either REST POST or MQTT
  --store-dir               directory to store results in for file protocol
  --read-dir                directory to read data to be sent
  --compress                Whether to compress create files, or decompress files being sent
  --api-key                 API key used for Linode (default) & Traffic data
  --linode-tag              group of linode nodes to get data from. If not gets from all nodes associated to token
  -e, --exception           whether or not to print exceptions to screen
```

### Examples 
* Ping & PercentageCPU Sensor types
  * Sample call to file 
  ```shell
  python3 data_generator.py 127.0.0.1:2049 ping file test 
  ```
  * Sample Data
  ```json
  {"timestamp": "2022-06-23T16:45:28.451182Z", "device_name": "Ubiquiti OLT", "parentelement": "d515dccb-58be-11ea-b46d-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw", "value": 35.41},
  {"timestamp": "2022-06-23T16:45:28.955278Z", "device_name": "Catalyst 3500XL", "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", "value": 47.08},
  {"timestamp": "2022-06-23T16:45:29.458781Z", "device_name": "Catalyst 3500XL", "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", "value": 3.61},
  {"timestamp": "2022-06-23T16:45:29.960486Z", "device_name": "VM Lit SL NMS", "parentelement": "1ab3b14e-93b1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H", "value": 8.85},
  {"timestamp": "2022-06-23T16:45:30.464822Z", "device_name": "GOOGLE_PING", "parentelement": "f0bd0832-a81e-11ea-b46d-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H", "value": 9.96},
  {"timestamp": "2022-06-23T16:45:30.968287Z", "device_name": "VM Lit SL NMS", "parentelement": "1ab3b14e-93b1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H", "value": 7.9},
  {"timestamp": "2022-06-23T16:45:31.468662Z", "device_name": "VM Lit SL NMS", "parentelement": "1ab3b14e-93b1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H", "value": 4.55},
  {"timestamp": "2022-06-23T16:45:31.973175Z", "device_name": "VM Lit SL NMS", "parentelement": "1ab3b14e-93b1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H", "value": 1.55},
  {"timestamp": "2022-06-23T16:45:32.474257Z", "device_name": "VM Lit SL NMS", "parentelement": "1ab3b14e-93b1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H", "value": 7.29},
  {"timestamp": "2022-06-23T16:45:32.978395Z", "device_name": "Catalyst 3500XL", "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", "value": 8.42}
  ```
  * AnyLog MQTT Client Call
  ```anylog
  <run mqtt client where broker=!ip and port=!anylog_broker_port and log=false topic=(
    name=!mqtt_topic_name and 
    dbms="bring [dbms]" and 
    table=ping_sensor and 
    column.timestamp.timestamp="bring [timestamp]" and 
    column.device_name=(type=str and value="bring [device_name]") and 
    column.parentelement=(type=str and value="bring [parentelement]") and 
    column.webid=(type=str and value="bring [webid]") and 
    column.value=(type=float and bring value="bring [value]")
  )>
  ```
* SIN & COS data 
  * Sample call using PUT 
  ```shell
  python3 data_generator.py 127.0.0.1:2049 cos put test  
  ```
  * Sample Data
  ```json
  {"timestamp": "2022-06-23T16:45:34.584943Z", "value": -1.2246467991473532e-16},
  {"timestamp": "2022-06-23T16:45:35.089708Z", "value": -1.0},
  {"timestamp": "2022-06-23T16:45:35.589965Z", "value": -0.8660254037844386},
  {"timestamp": "2022-06-23T16:45:36.093882Z", "value": -0.8414709848078965},
  {"timestamp": "2022-06-23T16:45:36.597142Z", "value": -0.7071067811865475},
  {"timestamp": "2022-06-23T16:45:37.100022Z", "value": -0.49999999999999994},
  {"timestamp": "2022-06-23T16:45:37.601919Z", "value": -0.3826834323650898},
  {"timestamp": "2022-06-23T16:45:38.106573Z", "value": 0.0}
  ```
  *   * AnyLog MQTT Client Call
  ```anylog
  <run mqtt client where broker=!ip and port=!anylog_broker_port and log=false topic=(
    name=!mqtt_topic_name and 
    dbms="bring [dbms]" and 
    table=cos_data and 
    column.timestamp.timestamp="bring [timestamp]" and  
    column.value=(type=float and bring value="bring [value]")
  )>
  ```