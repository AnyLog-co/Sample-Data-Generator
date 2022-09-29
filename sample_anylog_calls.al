#-----------------------------------------------------------------------------------------------------------------------
# Data Type: trig
# insert_process: post
# command: python3 Sample-Data-Generator/data_generator.py trig post test --conn 127.0.0.1:32149 --topic trig_data
#-----------------------------------------------------------------------------------------------------------------------
<run mqtt client where broker=rest and port=32149 and user-agent=anylog and log=false and topic=(
    name=trig_data and
    dbms=test and
    table=trig_data and
    column.timestamp.timestamp="bring [timestamp]" and
    column.value.float="bring [value]" and
    column.sin.float="bring [sin]" and
    column.cos.float="bring [cos]" and
    column.tan.float="bring [tan]"
)>

#-----------------------------------------------------------------------------------------------------------------------
# Data Type: power
# insert_process: Remote MQTT
# command: python3 Sample-Data-Generator/data_generator.py power mqtt test --conn ibglowct:MSY4e009J7ts@driver.cloudmqtt.com:18785 --topic power
#-----------------------------------------------------------------------------------------------------------------------
<run mqtt client where broker=driver.cloudmqtt.com and port=18785  and user=ibglowct and password=MSY4e009J7ts and log=false and topic=(
    name=power and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.location=(type=str and value="bring [location]") and
    column.value=(type=float and value="bring [value]" and optional=true) and
    column.phasor=(type=str and value="bring [phasor]" and optional=true) and
    column.source=(type=float and value="bring [source]" and optional=true) and
    column.frequency=(type=float and value="bring [frequency]" and optional=true) and
    column.dfreq=(type=float and value="bring [dfreq]" and optional=true)
)>
