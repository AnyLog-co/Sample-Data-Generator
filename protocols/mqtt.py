import random
from paho.mqtt import client as mqtt_client
import support


def mqtt_send_data(broker:str, port:int, topic:str, payloads:list, dbms:str, table:str=None, username:str=None, password:str=None):
    """
    Send data into an MQTT broker 
    :args:
        broker:str - MQTT broker IP
        port:int - MQTT broker port 
        topic:str - topic correlated to data
        payloads:list - either a dictionary or list of data being sent
        dbms:str - logical database to store data in
        table:str - table name to store data in
        username:str - MQTT broker user
        password:str - MQTT broker password correlated to user
    :params: 
        updated_payloads:list - either  
    """
    # connect to MQTT broker
    status = True
    mqtt_client_id = 'python-mqtt-%s' % random.randint(random.choice(range(0, 500)), random.choice(range(501, 1000)))
    try:
        mqtt = mqtt_client.Client(client_id=mqtt_client_id)
    except Exception as e:
        #print('Failed to create MQTT client (Error: %s)' % e)
        status = False
    else:
        try:
            mqtt.connect(host=broker, port=int(port))
        except Exception as e:
            #print('Failed to connect to MQTT broker %s:%s (Error: %s)' % (broker, port, e))
            status = False

    if status is True and username is not None and password is not None:
        try:
            mqtt.username_pw_set(username=username, password=password)
        except Exception as e:
            #print('Failed to set username and password (Error: %s)' % e)
            status = False
    if status is False:
        return status

    for payload in payloads:
        payload['dbms'] = dbms
        payload['table'] = table
        row = support.json_dumps(payload)
