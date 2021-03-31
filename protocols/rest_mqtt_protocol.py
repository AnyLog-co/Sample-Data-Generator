import json 
import requests 
from protocols import rest_protocol, mqtt_support 


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
        broker:str - MQTT broker 
        user:str - MQTT password   
        passwd:str - password for MQTT uusr 
    :output: 
       if success return True, else returns False 
    """
    sensor = table_name.split('_')[0] 
    status = [] 
    mqtt_cmd = 'mqtt publish where'

    broker, user, passwd = mqtt_support.extract_conn_info(mqtt_conn)

    mqtt_cmd += " broker=%s and port=%s" % (broker, mqtt_port) 
    if user != '': 
        mqtt_cmd += " and user=%s" % user 
    if passwd != '': 
        mqtt_cmd += " and password=%s" % passwd
    mqtt_cmd += (" and topic=%s" % mqtt_topic) + " and message=%s"
    for payload in payloads: 
        if sensor in ['ping', 'percentagecpu']: 
            message = mqtt_support.format_network_data(payload, dbms, table_name) 
        elif sensor == 'machine': 
            message = mqtt_support.format_machine_data(payload, dbms, table_name) 
        else:
            message = mqtt_support.format_trig_data(payload, dbms, table_name) 
        mqtt = mqtt_cmd %  message
        stat = __send_mqtt_cmd(conn, mqtt)
        status.append(stat) 

    if status.count(False)  > status.count(True):
        return False
    return True 

