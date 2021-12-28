# Data Generator 
The Sample-Data-Generator provides different types of data sets that users can store in their respecte database(s). 
The possible data sets are based on data set that were originally providd by different types of customers

### Requirements
   * [requests](https://pypi.org/project/requests)
   * [paho-mqtt](https://pypi.org/project/paho-mqtt/)
   * [pytz](https://pypi.org/project/pytz/)
   * [tzlocal](https://pypi.org/project/tzlocal/) 
   
### Deployment Process
Deployment can be done either cloning the code and installing the requirements or by downloading the docker image

**Options**: 
```bash
anylog@localhost:~/ $ python3 $HOME/Sample-Data-Generator/data_generator.py --help
  :positional arguments:
      conn                    REST IP + Port or broker IP + Port      (default: 127.0.0.1:2049)
      data-generator:str      data set to generate content for        (default: trig)
          * linode - content from linode
          * percentagecpu sensor data
          * ping sensor data
          * power data
          * synchrophasor data
          * trig (default)
      protocol                format to save data                     (default: file)
          * post
          * put
          * mqtt
          * file (default)
          * print 
      dbms                    logical database to store data in       (default: test)
  :optional arguments
      -h, --help                          show this help message and exit
      --repeat           REPEAT           number of time to repeat each batch, if 0 then run continuously
      --sleep            SLEEP            sleep time between each batch
      --batch-repeat     BATCH_REPEAT     number of rows per batch
      --batch-sleep      BATCH_SLEEP      sleep time between rows or a specific batch
      --topic            TOPIC            topic for MQTT or REST POST
      --timezone         TIMEZONE         Decide whether you want the timezone in UTC or local
          * utc   - actual UTC value
          * local - machine timestamp as UTC value
          * ET - +03:00 from UTC
          * BR - -03:00 from UTC
          * JP - +09:00 from UTC
          * WS - -09:00 from UTC
          * AU - +09:30 from UTC
          * IT - +01:00 from UTC
      --authentication   AUTHENTICATION   username, password
      --timeout TIMEOUT  REST             timeout (in seconds)
      --linode-token     LINODE_TOKEN     linode token
      --linode-tag       LINODE_TAG       group of linode nodes to get data from. If not gets from all nodes associated to token
      -e, -exception     EXCEPTION        whether or not to print exceptions to screen
```

**Python**: 
```bash 
anylog@localhost:~/ $ python3 $HOME/Sample-Data-Generator/data_generator.py 10.0.0.20:2048 ping print test --repeat 1 --sleep 0 --batch-repeat 5 --batch-sleep 0.5 --timezone AU --e  
{"timestamp": "2021-12-28 10:14:32.196300+09:30", "device_name": "ADVA FSP3000R7", "parentelement": "62e71893-92e0-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H", "value": 0.49, "dbms": "test", "table": "ping_sensor"}
{"timestamp": "2021-12-28 10:14:32.724828+09:30", "device_name": "ADVA FSP3000R7", "parentelement": "62e71893-92e0-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H", "value": 2.07, "dbms": "test", "table": "ping_sensor"}
{"timestamp": "2021-12-28 10:14:33.227768+09:30", "device_name": "Ubiquiti OLT", "parentelement": "d515dccb-58be-11ea-b46d-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw", "value": 13.1, "dbms": "test", "table": "ping_sensor"}
{"timestamp": "2021-12-28 10:14:33.731847+09:30", "device_name": "GOOGLE_PING", "parentelement": "f0bd0832-a81e-11ea-b46d-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H", "value": 32.97, "dbms": "test", "table": "ping_sensor"}
{"timestamp": "2021-12-28 10:14:34.234272+09:30", "device_name": "Ubiquiti OLT", "parentelement": "d515dccb-58be-11ea-b46d-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw", "value": 26.95, "dbms": "test", "table": "ping_sensor"}
```

**Docker**:
```bash
# pull code
docker pull anylog/sample-data-generator:latest

# Show params
docker run --name data-gen -e HELP=true --rm anylog/data-gen:latest

# Actual docker run
<< COMMENT
  1. For MQTT, PUT or POST "SAVE" format user should add "--network host" in the docker run command
  2. Instead of '--linode-token' use '-e TOKEN=?' and instead of '--linode-tag' use '-e TAG=?'
COMMENT >>    
docker run --name data-gen -e CONN=127.0.0.1:2048 -e GENERATOR=ping -e SAVE=print -e DBMS=test -e REPEAT=1 -e SLEEP=0 -e BATCH_REPEAT=5 -e BATCH_SLEEP=0.5 -e TIMEZONE=UTC --rm data-gen:latest
{"timestamp": "2021-12-28T00:58:30.503732Z", "device_name": "Catalyst 3500XL", "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", "value": 14.68, "dbms": "test", "table": "ping_sensor"}
{"timestamp": "2021-12-28T00:58:31.006234Z", "device_name": "GOOGLE_PING", "parentelement": "f0bd0832-a81e-11ea-b46d-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H", "value": 31.62, "dbms": "test", "table": "ping_sensor"}
{"timestamp": "2021-12-28T00:58:31.509024Z", "device_name": "Catalyst 3500XL", "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", "value": 42.58, "dbms": "test", "table": "ping_sensor"}
{"timestamp": "2021-12-28T00:58:32.011676Z", "device_name": "Catalyst 3500XL", "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw", "value": 28.42, "dbms": "test", "table": "ping_sensor"}
{"timestamp": "2021-12-28T00:58:32.514508Z", "device_name": "ADVA FSP3000R7", "parentelement": "62e71893-92e0-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H", "value": 2.7, "dbms": "test", "table": "ping_sensor"} 
```

### Data Sets
* **Network**
  * ping
  * percentagecpu
* **Power**
  * battery
  * eswitch
  * inverter
  * pmu
  * solar
  * synchrophasor - runs it's own process
* **Linode** - data stored on linode regarding devices
  * node_config - inserted via PUT and only on the first iteration
  * node_summary - inserted via PUT and only on the first iteration
  * io insight
  * cpu insight
  * public netv4
  * public netv6
* **Trig Data**
  * sin
  * cos

  
**Note**: When using either _POST_ or _MQTT_ to store the data, the accepting AnyLog node should contain a 
  `run mqtt client` process.

```anylog
# "run mqtt client" for POST command: 
run mqtt client where broker=rest and port=!anylog_server_port and user-agent=anylog and log=false and topic=!topic

# "run mqtt client" for MQTT command
run mqtt client where broker=!broker and port=!broker_port and user=!username and password=!password and log=false and topic=!topic

# topic for "linode" data sets 
topic=(name=!topic_name and dbms="bring [dbms]" and table="bring [table]" and column.timestamp.timestamp="bring [timestamp]" and column.member_id.int="bring [member_id]" and column.value.float="bring [value]")

# topic for "network" data sets
topic=(name=!topic_name and dbms="bring [dbms]" and table="bring [table]" and column.timestamp.timestamp="bring [timestamp]" and column.device_name.str="bring [device_name]" and column.parentelement.str="bring [parentelement]" and column.webid.str="bring [webid]" and column.value.float="bring [value]") 

# topic for "power" data sets  
topic=(name=!topic_name and dbms="bring [dbms]" and table="bring [table]" and column.timestamp.timestamp="bring [timestamp]" and column.location.str="bring [location] and column.value.float="bring [value]")

# topic for "synchrophasor" data set 
topic=(name=!topic_name and dbms="bring [dbms]" and table="bring [table]" and column.timestamp.timestamp="bring [timestamp]" and column.location.str="bring [location] and column.sequence.int="bring [sequence]" and column.phasor.str="bring [phasor]" and column.frequency.float="bring [frequency]" and column.dfreq.float="bring [dfreq]")

# Trig data sets
topic=(name=!topic_name and dbms="bring [dbms]" and table="bring [table]" and column.timestamp.timestamp="bring [timestamp]" and column.value.float="bring [value]")
```

