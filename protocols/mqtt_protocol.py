"""
The following is code is based on: 
--> https://www.emqx.io/blog/how-to-use-mqtt-in-python
--> http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
"""
import json 
import random 
import time

from paho.mqtt import client as mqtt_client
from protocols import mqtt_support

def connect_mqtt(conn:str, port:int)->mqtt_client.Client:
    """
    The following code connects to MQTT for publishing
    :args:
       conn:str  - MQTT connection info (user@broker:passwd) 
       port:str  - MQTT port 
    :param:
       client:mqtt_client.Client- MQTT client connection 
       broker:str - IP from conn 
       user:str - Username from conn (optional) 
       passwd:str - password for conn (optional) 
       client_id:str - unique ID 
    :return: 
       connection to MQTT if success, else none
    """
    broker, user, passwd = mqtt_support.extract_conn_info(conn)

    client_id = 'python-mqtt-%s' % random.randint(random.choice(range(0, 500)), random.choice(range(501, 1000)))

    try: 
        client = mqtt_client.Client(client_id)
    except Exception as e:
        print('Failed to set connection Client ID (Error: %s)' % e) 
        client = None
    
    if client != None and user != '' and passwd != '': 
        try:
            client.username_pw_set(user, passwd)
        except Exception as e: 
            print('Failed to set username & password for MQTT (Error: %s)' % e) 

    if client != None:
        try:
            client.connect(broker, port)
        except Exception as e: 
            print('Failed to connect to broker on host: %s & port: %s (Error: %s)' % (broker, port, e))
            client = None 
    return client

def publisher_message(client:mqtt_client.Client, qos_value:int, topic:str, message:str)->bool:
    """
    Publish messages via MQTT 
    :args:
       client:mqtt_client.Client - connection to MQTT publisher
       topic:str - MQTT topic info 
       qos_value:int - MQTT Quality of Service 
       message:str - message to send to broker 
    :param:
       status:bool - status
    :return:
       If success True, else False 
    """
    status = True 
    if isinstance(message, dict):
        message = json.dumps(message)
    if not isinstance(message, str) and not isinstance(message, (float, int)):
        print('Invalid message "%s" due to %s data-type' % (message, type(message)))
        status = False

    try: 
        result = client.publish(topic, message, qos=qos_value, retain=False)
    except Exception as e: 
        print('Failed to publisher message: "%s" (Error: %s)' % (message, e))
        status = False 
    time.sleep(5)
    #print(topic, message, qos_value, result) 
    if result[0] != 0: 
        status = False 
        
    return status 

def publish_mqtt(conn:str, port:int, qos_value:int, topic:str, dbms:str, table_name:str, payloads:list)->bool:
    """
    Publish data directly to MQTT broker
    :args:
       conn:str - MQTT Connection info (IP) 
       port:int - MQTT port number 
       qos_value:int - MQTT Quality of Service 
       topic:str - MQTT topic 

       dbms:str - database name 
       table_name:str - table_name 
       payloads:list - list of data to send 
    :param:
       mqtt_conn:mqtt_client.Client - MQTT connection 
       broker:str - broker info from conn 
    :return:
       if success return True, else return False
    """
    status = []
    mqtt_conn = connect_mqtt(conn, port)  
    if mqtt_conn is None: 
        return False 

    for payload in payloads: 
        if table_name in ['ping_sensor', 'percentagecpu_sensor']: 
            message = mqtt_support.format_network_data(payload, dbms, table_name) 
        elif table_name == 'machine_data': 
            message = mqtt_support.format_machine_data(payload, dbms, table_name) 
        else:
            message = mqtt_support.format_trig_data(payload, dbms, table_name) 
        status.append(publisher_message(mqtt_conn, qos_value, topic, message))

    if status.count(False)  > status.count(True):
        return False
    return True 

