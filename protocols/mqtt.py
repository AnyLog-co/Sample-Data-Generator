import random
from paho.mqtt import client
import support
import time


def connect_mqtt_broker(broker:str, port:int, username:str=None, password:str=None, exception:bool=True):
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
        mqtt_client = client.Client(mqtt_client_id)
    except Exception as e:
        if exception is True:
            print('Failed to set MQTT client ID (Error: %s)' % e)
        mqtt_client = None

    # set username and password
    if mqtt_client is not None and username is not False and password is not None:
        try:
            mqtt_client.username_pw_set(username, password)
        except Exception as e:
            if exception is True:
                print('Failed to set MQTT username & password (Error: %s)' % e)
            mqtt_client = None

    # connect to broker
    if mqtt_client is not None:
        try:
            mqtt_client.connect(broker, int(port))
        except Exception as e:
            if exception is True:
                print('failed to connect to MQTT broker %s against port %s (Error: %s)' % (broker, port, e))
            mqtt_client = None

    return mqtt_client


def send_data(mqtt_client:client.Client, topic:str, data:dict, dbms:str, table:str, exception:bool=False)->bool:
    """
    Send data into an MQTT broker
    :args:
        mqtt_client:paho.mqtt.client.Client - MQTT broker client
        topic:str - topic to send data into
        data:dict - either list or dict of data to send into MQTT broker
        dbms:str - logical database
        table:str - logical table name
        exception:bool - whether or not to print exceptions
    :params:
        status:bool
        payloads:list - converted data
        r:paho.mqtt.client.MQTTMessageInfo - result from publish process
    :return:
        status
    """
    status = True
    payloads = support.payload_conversions(payloads=data, dbms=dbms, table=table)
    for message in payloads:
        try:
            r = mqtt_client.publish(topic, message, qos=1, retain=False)
        except Exception as e:
            if exception is True:
                print(f'Failed to publish results in {mqtt_client} (Error: {e})')
            status = False
        else:
            time.sleep(5)
            if r[0] != 0 and exception is True:
                print('There was a network error when publishing content')
                status = False
            elif r[0] != 0:
                status = False

    return status






