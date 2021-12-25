import random
from paho.mqtt import client as mqtt_client
import convert_json


def mqtt_data(broker:str, port:int, topic:str, data:list, dbms:str, table:str=None, username:str=None, password:str=None)->bool:
    """
    Send data into an MQTT broker
    :notes:
        URL: https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#configuring-an-anylog-node-as-a-message-broker
        note:
            * an MQTT client that with broker set to local if deploying AnyLog as a broker (run message broker ${IP} ${BROKER_PORT)
            * an MQTT client that with broker set to URL if deploying any other MQTT broker
    :args:
        broker:str - MQTT broker info
        port:int - MQTT broker port
        topic:str - MQTT topic
        data:list - data to send into MQTT
        username:str - MQTT username
        password:str - MQTT password
    :params:
        status:bool
        mqtt_client_id:str - unique client id string used when connecting to the broker
        cur - connection to MQTT client
        payload:str - content to post to MQTT
    """
    status = True
    mqtt_client_id = 'python-mqtt-%s' % random.randint(random.choice(range(0, 500)), random.choice(range(501, 1000)))

    try:
        cur = mqtt_client.Client(client_id=mqtt_client_id)
    except Exception as e:
        status = False
        print('Failed to declare client connection (Error: %s)' % e)
    else:
        try:
            cur.connect(host=broker, port=port)
        except Exception as e:
            status = False
            print('Failed to connect client to MQTT broker %s:%s (Error: %s)' % (broker, port, e))

    if status is True and username is not None and password is not None:
        try:
            cur.username_pw_set(username=username, password=password)
        except Exception as e:
            status = False
            print('Failed to set username [%s] and password [%s] for connection (Error: %s)' % (username, password, e))

    if status is False:
        return status

    if isinstance(data, list):
        for row in data:
            row['dbms'] = dbms
            row['table'] = table
            payload = convert_json.json_dumps(row)
            try:
                cur.publish(topic=topic, payload=payload, qos=1, retain=False)
            except Exception as e:
                status = False
    elif isinstance(data, dict):
        for table in data:
            for row in data[table]:
                row['dbms'] = dbms
                row['table'] = table
                payload = convert_json.json_dumps(row)
                try:
                    cur.publish(topic=topic, payload=payload, qos=1, retain=False)
                except Exception as e:
                    status = False

    return status
