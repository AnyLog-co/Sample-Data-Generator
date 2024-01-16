import json
import random
import sys
import time

is_mqtt = True
try:
    from paho.mqtt import client
except:
    is_mqtt = False


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


class AnyLogMQTT:
    def __init__(self, conns:str, qos:str, exception:bool=False):
        self.qos = qos
        self.conns = {}
        self.exception = exception

        for conn in conns.split(","):
            broker, port = conn.split("@")[-1].split(":")
            user = None
            password = None
            if '@' in conn:
                user, password = conn.split("@")[0].split(":")
            self.conns['al-mqtt-%s' % random.choice(list(range(500, 1001)))] = {
                'broker': broker,
                'port': int(port),
                'user': user,
                'password': password
            }

        if is_mqtt is False:
            print("paho-mqtt is not installed. Cannot continue...")
            exit(1)


    def __wait(self, msg_size:float):
        """
        Based on message size, wait n seconds
        """
        wait_time = int(msg_size / 2048) + 1
        if wait_time > 60:
            wait_time = 60
        time.sleep(wait_time)


    def connect_mqtt_client(self, client_id:str):
        """
        Connect to MQTT broker
        :args:
            client_id:str - MQTT broker client ID
        :global:
            self.mqtt_client:client.Client - connection to broker
        :params:
            broker:str - MQTT broker IP
            port:int - MQTT broker port
            user:str - user for broker connection
            password:str - password associated with user
        """
        self.mqtt_client = None
        broker = self.conns[client_id]['broker']
        port = self.conns[client_id]['port']
        user = self.conns[client_id]['user']
        password = self.conns[client_id]['password']

        try:
            self.mqtt_client = client.Client(client_id=client_id)
        except Exception as error:
            self.mqtt_client = None
            if self.exception is True:
                print(f'Failed to set MQTT client ID (Error: {error})')

        if all(None is not x for x in [self.mqtt_client, user, password]):
            try:
                self.mqtt_client.username_pw_set(username=user, password=password)
            except Exception as error:
                self.mqtt_client = None
                if self.exception is True:
                    print(f'Failed to set MQTT username & password (Error: {error})')

        if self.mqtt_client is not None:
            try:
                self.mqtt_client.connect(host=broker, port=port)
            except Exception as error:
                self.mqtt_client = None
                if self.exception is True:
                    print('failed to connect to MQTT broker %s against port %s (Error: %s)' % (broker, port, error))


    def disconnect_mqtt_client(self, client_id):
        """
        Disconnect from MQTT client
        :args:
            client_id:str - MQTT broker client ID
        :params:
            conn_info:str - connection information
        """
        conn_info = f"{self.conns[client_id]['broker']}:{self.conns[client_id]['port']}"
        try:
            self.mqtt_client.disconnect()
        except Exception as error:
            if self.exception is True:
                print(f"Failed to disconnect from {conn_info} (Error: {error})")

    def send_data(self, payloads:list, topic:str):
        message = json.dumps(payloads)

        try:
            r = self.mqtt_client.publish(topic, message, self.qos)
        except Exception as error:
            if self.exception is True:
                print(f'Failed to publish results in {self.mqtt_client} (Error: {error})')
        else:
            self.__wait(msg_size=sys.getsizeof(message))
            if r[0] != 0:
                if self.exception is True:
                    error_msg = "Unknown"
                    if r[0] in MQTT_ERROR_CODES:
                        error_msg = MQTT_ERROR_CODES[r[0]]
                    print(f"There was a network error when publishing content (Error Code: {r[0]} - {error_msg})")

    def publish_data(self, payloads:list, topic:str):
        client_id = random.choice(list(self.conns))
        self.connect_mqtt_client(client_id=client_id)

        if self.mqtt_client is None:
            if self.exception is True:
                print(f"Failed to connect to MQTT broker")
            return

        self.mqtt_client.loop_start()
        self.send_data(payloads=payloads, topic=topic)
        self.mqtt_client.loop_stop()
        self.disconnect_mqtt_client(client_id=client_id)
