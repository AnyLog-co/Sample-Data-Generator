from paho.mqtt import client as mqtt_client
import random 

def connect_mqtt(conn:str, port:int, topic:str)->paho.mqtt.client.Client:
    """
    The following code connects to MQTT for publishing
    :args:
       conn:str  - MQTT connection info (user@broker:passwd) 
       port:str  - MQTT port 
       topic:str - MQTT topic 
    :param:
       client:paho.mqtt.client.Client- MQTT client connection 
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

if __name__ == '__main__': 
    mqtt_conn = connect_mqtt('ibglowct@driver.cloudmqtt.com:MSY4e009J7ts', 18785, 'anylogedgex') 
    print(type(mqtt_conn))
