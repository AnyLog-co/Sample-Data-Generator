import json 
import requests 
#from rest_protocol import validate_connection



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
    :smaple-output: 
        machine: {'value': {'hostname': 'os-anylog-develop', 'local_ip': '10.0.0.89', 'remote_ip': '24.23.250.144', 'boot_time': 25460.645260095596, 'cpu_percentage': 29.6, 'swap_memory': 0.0, 'disk_usage': 0.0}, 'ts': '2021-03-26 00:17:44.437186', 'metadata': {'protocol': None, 'company': 'dmci', 'machine_name': 'machine', 'serial_number': 'data'}, 'protocol': 'system info'}

        trig: {'value': -1.9476794448335322, 'ts': '2021-03-26 00:19:25.223752', 'metadata': {'protocol': None, 'company': 'dmci', 'machine_name': 'rand', 'serial_number': 'data'}, 'protocol': 'trig'}
        networking: {'value': 43, 'ts': '2021-03-26 00:19:46.222511', 'metadata': {'protocol': None, 'company': 'dmci', 'machine_name': 'ping', 'serial_number': 'sensor'}, 'protocol': 'networking'}
    """
    message = {
        "value": None,
        "ts": None,
        "metadata":{
            "protocol": None,
            "company": dbms, 
            "machine_name": sensor,
            "serial_number": None
        }
    }
    if sensor in ['ping', 'percentagecpu']: 
        message['value'] = payload['value']
        message['ts'] = payload['timestamp'] 
        message['metadata']['protocol'] = 'networking' 
        message['metadata']['serial_number'] = 'sensor'  
    elif sensor in ['sin', 'cos', 'rand']: 
        message['value'] = payload['value']
        message['ts'] = payload['timestamp'] 
        message['metadata']['protocol'] = 'trig' 
        message['metadata']['serial_number'] = 'data'  
    elif sensor == 'machine': 
        message['ts'] = payload['timestamp'] 
        del payload['timestamp'] 
        message['value'] = payload 
        message['metadata']['protocol'] = 'system info' 
        message['metadata']['serial_number'] = 'data'  

    return message

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

def mqtt_protocol(payloads:list, conn:str, dbms:str, table_name:str, mqtt_conn:str, mqtt_port:int, mqtt_topic:str)->bool:
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
    :param: 
        sensor:str - from table name get sensor name 

        mqtt_cmd:str - command to execute MQTT 
        mqtt_broker:str - MQTT broker 
        mqtt_user:str - MQTT password   
        mqtt_passwd:str - password for MQTT uusr 

    :sample call: 
        headers = {
            'type': 'info',
            'details': 'mqtt publish where broker=driver.cloudmqtt.com and port=18975 and user=mqwdtklv and password="uRimssLO4dIo" and topic=test and message= {"value": -1.2246467991473532e-16, "ts": "2021-01-10 02:00:34.553093", "protocol": "trig", "measurement": "sin", "metadata": {"company": "test", "machine_name": "sin", "serial_number": "data"}}'
    :output: 
       if success return True, else returns False 
    """
    #if not validate_connection(conn): 
    #    return False 

    sensor = table_name.split('_')[0] 
    statuses = [] 
    status = True 

    mqtt_broker = mqtt_conn.split('@')[1].split(':')[0] 
    mqtt_user = mqtt_conn.split('@')[0] 
    mqtt_passwd = mqtt_conn.split(':')[-1] 
    statuses = [] 

    mqtt_cmd = 'mqtt publish where broker=%s and port=%s and user=%s and password="%s" and topic=%s and message=%s'
    for payload in payloads: 
        message = __mqtt_format(payload, dbms, sensor)
        mqtt = mqtt_cmd % (mqtt_broker, mqtt_port, mqtt_user, mqtt_passwd, mqtt_topic, message) 
        stat = __send_mqtt_cmd(conn, mqtt)
        statuses.append(stat) 

    if False in statuses: 
        status = False 
    return status
