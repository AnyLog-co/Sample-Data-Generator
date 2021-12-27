import random
from paho.mqtt import client as mqtt_client
import support


def connect_mqtt_broker(broker:str, port:int, username:str=None, password:str=None, exception:bool=True)->paho.mqtt.client.Client:
    """
    Connect to an MQTT broker
    :args:
        broker:str - MQTT broker IP
        port:int - MQTT broker port
        username:str - MQTT broker user
        password:str - MQTT broker password correlated to user
    :params: 
        mqtt_client_id:str - MQTT client ID
        client:paho.mqtt.client.Client - MQTT client object
    :return:
        client
    """
    # connect to MQTT broker
    status = True
    mqtt_client_id = 'python-mqtt-%s' % random.randint(random.choice(range(0, 500)), random.choice(range(501, 1000)))

    try:
        client = mqtt_client.Client(mqtt_client_id)
    except Exception as e:
        if exception is True:
            print('Failed to set MQTT client ID (Error: %s)' % e)
        client = None

    # set username and password
    if client is not None and username is not False and password is not None:
        try:
            client.username_pw_set(username, password)
        except Exception as e:
            if exception is True:
                print('Failed to set MQTT username & password (Error: %s)' % e)
            client = None

    # connect to broker
    if client is not None:
        try:
            client.connect(broker, int(port))
        except Exception as e:
            if exception is True:
                print('failed to connect to MQTT broker %s against port %s (Error: %s)' % (broker, port, e))
            client = None

    return client

def send_data(mqtt_client:paho.mqtt.client.Client, topic:str, payloads:dict, dbms:str, table:str)->(bool, int):
    """

    """
    pass




