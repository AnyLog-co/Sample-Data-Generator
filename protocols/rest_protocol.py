import json 
import requests 

def __mqtt_format(payload:dict, dbms:str, sensor:str)->str: 
    """
    The following converts data into MQTT formatted object
    :args: 
        payload:dict - data to send via MQTT 
        dbms:str - database name
        sensor:str - sensor name 
    :param: 
        message:dict - MQTT object to send 
    :MQTT Format: 
        dbms=!company_name 
        table = "bring [metadata][machine_name] _ [metadata][serial_number]" 
        column.timestamp.timestamp = "bring [ts]" 
        column.value.int = "bring [value]")
    :return: 
        JSON formatted mesesage 
    """

    message = {
        "value": payload['value'],
        "ts": payload['timestamp'],
        "protocol":"trig",
        "measurement": sensor,
        "metadata":{
            "company": dbms, 
            "machine_name": sensor,
            "serial_number": "data"
        }
    }

    return json.dumps(message)

def __send_mqtt_cmd(conn:str, cmd:str)->bool: 
   """
   Validate node is accessible
   :args: 
      conn:str - connection string 
   :param:
      boolean:bool - boolean status 
   :return: 
      if node is accessible return True, else return False 
   """
   boolean = False 
   header = { 
      "type": "info", 
      "details": cmd
   }
   
   print(header) 
   try:
      r = requests.get('http://%s' % conn, headers=header)
   except Exception as e: 
      print(e) 

   print(r) 
   exit(1) 

   return boolean

def validate_connection(conn:str)->bool: 
   """
   Validate node is accessible
   :args: 
      conn:str - connection string 
   :param:
      boolean:bool - boolean status 
   :return: 
      if node is accessible return True, else return False 
   """
   boolean = False 
   try:
      r = requests.get('http://%s' % conn, headers={'type': 'info', 'details': 'get status'})
   except Exception as e: 
      print(e) 

   if 'running' in r.json()['Status']:
      boolean=True  
   return boolean 


def send_data(payloads:list, conn:str, dbms:str, table_name:str, mode:str)->bool:
    """
    Send payload to node via REST 
    :args: 
        payloads:dict - data to store in database 
        conn:str - connection string 
        dbms:str - logical database to store data in 
        table_name:str - logical table to store data in 
        mode:str - format by which to send data via REST 
    :param:
        header:dict - REST PUT header info        
    """
    header = { 
        'type': 'json', 
        'dbms': dbms, 
        'table': table_name,
        'mode': mode, 
        'Content-Type': 'text/plain'
    }
    status=True 
    for payload in payloads: 
        json_payload = json.dumps(payload) 
        try: 
            requests.put('http://%s' % conn, headers=header, data=json_payload)
        except Exception as e:
            print(e) 
            status=False  
    return status

def mqtt_protocol(payloads:list, conn:str, dbms:str, table_name:str, mqtt_conn:str, mqtt_port:int, mqtt_topic:str)->bool:
    """
    Store data via MQTT protocol 
    :Steps: 
        1. Create MQTT publish command 
        2.  
    :args:
        payloads:list - data to send via MQTT 
        conn:str - REST conn IP + Port 
        dbms:str - database name (used for company name) 
        table_name:str - table name 

        mqtt_conn:str - MQTT usr@ip:passwd 
        mqtt_port:int - Port for MQTT
        mqtt_topic:str - MQTT topic 
    :param: 
        sensor:str - from table name get sensor name 

        mqtt_cmd:str - command to execute MQTT 
        mqtt_broker:str - MQTT broker 
        mqtt_user:str - MQTT password   
        mqtt_passwd:str - password for MQTT uusr 
    """
    sensor = table_name.split('_')[0] 
    
    mqtt_broker = mqtt_conn.split('@')[1].split(':')[0] 
    mqtt_user = mqtt_conn.split('@')[0] 
    mqtt_passwd = mqtt_conn.split(':')[-1] 

    mqtt_cmd = "mqtt publish where broker=%s and port=%s and user=%s and password=%s and topic=%s and message=%s" 
    for payload in payloads: 
        message = __mqtt_format(payload, dbms, sensor)
        mqtt = mqtt_cmd % (mqtt_broker, mqtt_port, mqtt_user, mqtt_passwd, mqtt_topic, message) 
        print(mqtt)
        status = __send_mqtt_cmd(conn, mqtt)

