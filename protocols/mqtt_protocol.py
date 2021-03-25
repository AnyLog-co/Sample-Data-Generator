# The following is based on: https://www.emqx.io/blog/how-to-use-mqtt-in-python
import json 
from paho.mqtt import client as mqtt_client
import random 

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
    try: 
        broker = conn.split('@')[1].split(':')[0]
    except: 
        broker = conn 
    try: 
        user = conn.split('@')[0]
    except:
        user = '' 
    try: 
        passwd = conn.split(':')[1] 
    except:
        passwd = '' 

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

def publisher_message(client:mqtt_client.Client, topic:str, message:str)->bool:
    """
    Publish messages via MQTT 
    :args:
       client:mqtt_client.Client - connection to MQTT publisher
       topic:str - MQTT topic info 
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
        result = client.publish(topic, message)
    except Exception as e: 
        print('Failed to publisher message: "%s" (Error: %s)' % (message, e))
        status = False 
        
    if result[0] != 0: 
        status = False 
        
    return status 

if __name__ == '__main__': 
    mqtt_conn = connect_mqtt('10.0.0.89', 2050)  
    print(publisher_message(mqtt_conn, 'demo', '{"value": "-1.0", "ts": "2021-03-25 04:07:50.932658", "protocol": "trig", "measurement": "cos", "metadata": {"company": "litsanleandro", "machine_name": "cos", "serial_number": "data"}}'))
