import random
import sys
import time
from data_generator.support import serialize_data
try:
    import paho.mqtt as mqtt
except:
    pass

MQTT_ERROR_CODES = { # based on: https://www.vtscada.com/help/Content/D_Tags/D_MQTT_ErrMsg.htm + ChatGTP information
    -1: "MQTT_ERR_NO_CONN",
    1: "Connection Refused: Unacceptable protocol version",
    2: "Connection Refused: Identifier rejected",
    3: "Connection Refused: Server Unavailable",
    4: "Connection Refused: Bad username or password",
    5: "Connection Refused: Authorization error",
    6: "Connection lost or bad",
    7: "Timeout waiting for Length bytes",
    8: "Timeout waiting for Payload",
    9: "Timeout waiting for CONNACK",
    10: "Timeout waiting for SUBACK",
    11: "Timeout waiting for UNSUBACK",
    12:	"Timeout waiting for PINGRESP",
    13: "Malformed Remaining Length",
    14: "Problem with the underlying communication port",
    15: "Address could not be parsed",
    16:	"Malformed received MQTT packet",
    17:	"Subscription failure",
    18:	"Payload decoding failure",
    19:	"Failed to compile a Decoder",
    20:	"The received MQTT packet type is not supported on this client",
    21:	"Timeout waiting for PUBACK",
    22:	"Timeout waiting for PUBREC",
    23:	"Timeout waiting for PUBCOMP",
    39: "MQTT_ERR_PAYLOAD_SIZE",
    0x18: "MQTT_ERR_REFUSED_BAD_USERNAME_OR_PASSWORD",
    0x21: "MQTT_ERR_REFUSED_IDENTIFIER_REJECTED",
    0x24: "MQTT_ERR_REFUSED_NOT_AUTHORIZED",
    0x80: "MQTT_ERR_REFUSED",
}

def __wait(message_size:int):
    wait_time = int(message_size / 2048) + 1
    if wait_time > 60:
        wait_time = 60
    time.sleep(wait_time)


def __connect_mqtt_broker(broker:str, port:int, username:str=None, password:str=None, exception:bool=False):
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
        mqtt_client = mqtt.Client(mqtt_client_id)
    except Exception as e:
        if exception is True:
            print('Failed to set MQTT client ID (Error: %s)' % e)
        mqtt_client = None

    # set username and password
    if mqtt_client is not None and username is not None and password is not None:
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



def __disconnect_mqtt(conn_info:str, mqtt_conn:client.Client, exception:bool=False)->bool:
    """
    Disconnect from MQTT client
    :args:
        mqtt_conn:paho.mqtt.client.Client - connection to MQTT
        exception:bool - whether to print exception
    :params:
        status:bool
    :return:
        status
    """
    status = True

    try:
        mqtt_conn.disconnect()
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to disconnect from {conn_info} (Error: {error})")

    return status


def __publish_payload(mqtt_client:mqtt.Client, topic:str, message:str, qos:int=0, exception:bool=False)->bool:
    """
    Send data into an MQTT broker
    :args:
        mqtt_client:paho.mqtt.client.Client - MQTT broker client
        topic:str - topic to send data into
        data:dict - either list or dict of data to send into MQTT broker
        dbms:str - logical database
        table:str - logical table name
        exception:bool - whether to print exceptions
    :params:
        status:bool
        payloads:list - converted data
        r:paho.mqtt.client.MQTTMessageInfo - result from publish process
    :return:
        status
    """
    status = True
    try:
        r = mqtt_client.publish(topic, message, qos=qos, retain=False)
    except Exception as e:
        if exception is True:
            print(f'Failed to publish results in {mqtt_client} (Error: {e})')
        status = False
    else:
        __wait(message_size=sys.getsizeof(message))
        if r[0] != 0:
            if exception is True:
                error_msg = "Unknown"
                if r[0]in MQTT_ERROR_CODES:
                    error_msg = MQTT_ERROR_CODES[r[0]]
                print(f"There was a network error when publishing content (Error Code: {r[0]} - {error_msg})")
            status = False

    return status


def publish_mqtt(conn:str, payload:list, topic:str, qos:int=0, auth:tuple=(), exception:bool=False):
    broker, port = conn.split(":")
    username, password = auth

    serialized_payload = serialize_data(payload=payload)
    mqtt_client = __connect_mqtt_broker(broker=broker, port=port, username=username, password=password, exception=exception)

    if mqtt_client is not None:
        mqtt_client.loop_start()
        status = __publish_payload(mqtt_client=mqtt_client, message=serialized_payload, topic=topic, qos=qos, exception=exception)
        if status is True:
            # stop loop
            mqtt_client.loop_stop()
            __disconnect_mqtt(conn_info=f"{broker}:{port}", mqtt_conn=mqtt_client, exception=exception)



