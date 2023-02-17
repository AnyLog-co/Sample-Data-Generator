import random
from paho.mqtt import client
import support

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


def connect_mqtt_broker(broker:str, port:int, username:str=None, password:str=None, exception:bool=True)->client.Client:
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


def disconnect_mqtt(conn_info:str, mqtt_conn:client.Client, exception:bool=False)->bool:
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


def send_data(mqtt_client:client.Client, topic:str, message:str, exception:bool=False)->bool:
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
    try:
        r = mqtt_client.publish(topic, message, qos=0, retain=False)
    except Exception as e:
        if exception is True:
            print(f'Failed to publish results in {mqtt_client} (Error: {e})')
        status = False
    else:
        if r[0] != 0:
            if exception is True:
                error_msg = "Unknown"
                if r[0]in MQTT_ERROR_CODES:
                    error_msg = MQTT_ERROR_CODES[r[0]]
                print(f"There was a network error when publishing content (Error Code: {r[0]} - {error_msg})")
            status = False
            
    return status


def mqtt_process(mqtt_client:client.Client, payloads:list, topic:str, exception:bool=True)->bool:
    """
    Main for MQTT process
    :args:
        payloads:list - content to send into MQTT
        topic:str - MQTT topic name
        broker:str - MQTT broker address
        port:int - IP associated with broker
        username:str - User associated with MQTT connection information
        password:str - password associated with user
        exception:bool - whether to print exception
    :params:
        status:bool
        mqtt_client:client.Client - MQTT client connection
        str_payloads:str - JSON string of payloads
    :return:
        status
    """
    status = True

    if isinstance(payloads, list):
        for payload in payloads:
            str_payloads = support.json_dumps(payloads=payload)
            if send_data(mqtt_client=mqtt_client, topic=topic, message=str_payloads, exception=exception) is False:
                status = False
    elif isinstance(payloads, dict):
        str_payloads = support.json_dumps(payloads=payloads)
        if send_data(mqtt_client=mqtt_client, topic=topic, message=str_payloads, exception=exception) is False:
            status = False
    else:
        status = False
        if exception is True:
            print(f"Invalid payload in format {type(payloads)}")

    return status

