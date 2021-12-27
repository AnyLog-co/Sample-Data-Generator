# Data Generator 
The Sample-Data-Generator provides different types of data sets that users can store in their respecte database(s). 
The possible data sets are based on data set that were originally providd by different types of customers

### Requirements
   * [requests](https://pypi.org/project/requests)
   * [paho-mqtt](https://pypi.org/project/paho-mqtt/)
   

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
  `run mqtt client` process. (The topic name correlate to the _data-generator_ value)

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

 
