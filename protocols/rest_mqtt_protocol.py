import json 
import requests 
from protocols import rest_protocol, mqtt_format


def __send_mqtt_cmd(conn:str, cmd:str)->bool: 
   """
   Validate node is accessible
   :args: 
      conn:str - connection string 
   :param:
      boolean:bool - boolean status 
   :return: 
      if node is accessible return True, else return False 
   :sample cURL: 
      curl --location --request POST 10.0.0.89:2049 \
              --header 'User-Agent: AnyLog/1.23' \
              --header 'command: mqtt publish where broker=driver.cloudmqtt.com and port=18975 and user=mqwdtklv and password=uRimssLO4dIo and topic=test and message={"value": "-1.0", "ts": "2021-03-25 04:07:50.932658", "protocol": "trig", "measurement": "cos", "metadata": {"company": "litsanleandro", "machine_name": "cos", "serial_number": "data"}}'
   """
   boolean = True 
   header = { 
      "User-Agent": "AnyLog/1.23", 
      "command": cmd
   }
   try:
      r = requests.post('http://%s' % conn, headers=header)
   except Exception as e: 
      print('Failed to post MQTT request to %s. (Error: %s)' % (conn, e)) 
      boolean = False 
   try: 
      if int(r.status_code) != 200:
         boolean = False 
   except Exception as e: 
      print('Error: %s' % e) 
      boolean = False 

   return boolean

def mqtt_protocol(payloads:list, conn:str, dbms:str, table_name:str, mqtt_conn:str, mqtt_port:int, mqtt_topic:str, anylog_broker:bool)->bool:
    """
    Send requests to MQTT broker via AnyLog using REST call 
    :Steps: 
        1. Create MQTT publish command 
        2. Send command via REST 
        3. Command gets executed on AnyLog instance 
    :args:
        payloads:list - data to send via MQTT 
        conn:str - REST conn IP + Port 
        dbms:str - database name (used for company name) 
        table_name:str - table name 

        mqtt_conn:str - MQTT usr@ip:passwd 
        mqtt_port:int - Port for MQTT
        mqtt_topic:str - MQTT topic 

        anylog_broker:bool - AnyLog acts as broker 
    :param: 
        sensor:str - from table name get sensor name 

        mqtt_cmd:str - command to execute MQTT 
        mqtt_broker:str - MQTT broker 
        mqtt_user:str - MQTT password   
        mqtt_passwd:str - password for MQTT uusr 
    :output: 
       if success return True, else returns False 
    """
    sensor = table_name.split('_')[0] 
    status = [] 
     
    try:  
        mqtt_broker = mqtt_conn.split('@')[1].split(':')[0] 
    except: 
        mqtt_broker = mqtt_conn 

    mqtt_cmd = 'mqtt publish where broker=%s and port=%s and topic=%s and message=%s'
    if anylog_broker is False: 
        mqtt_user = mqtt_conn.split('@')[0] 
        mqtt_passwd = mqtt_conn.split(':')[-1] 
        mqtt_cmd = 'mqtt publish where broker=%s and port=%s and user=%s and password="%s" and topic=%s and message=%s'

    if not rest_protocol.validate_connection(conn): 
        return False 

    for payload in payloads: 
        if sensor in ['ping', 'percentagecpu']: 
            message = mqtt_format.format_network_data(payload, dbms, sensor) 
        elif sensor == 'machine': 
            message = mqtt_format.format_machine_data(payload, dbms, sensor) 
        else:
            message = mqtt_format.format_trig_data(payload, dbms, sensor) 

        if anylog_broker is False: 
            mqtt = mqtt_cmd % (mqtt_broker, mqtt_port, mqtt_user, mqtt_passwd, mqtt_topic, message) 
        else: 
            mqtt = mqtt_cmd % (mqtt_broker, mqtt_port, mqtt_topic, message) 
        stat = __send_mqtt_cmd(conn, mqtt)
        status.append(stat) 

    if status.count(False)  > status.count(True):
        return False
    return True 

