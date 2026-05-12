import json
import time
try:
    import paho.mqtt.client as mqtt
except ImportError:
    _missing_mqtt = True
else:
    _missing_mqtt = False

from typing import List
from source.northbound.error_codes import MQTT_ERROR_CODES


class MqttClient:
    """
    MQTT client wrapper for connecting, publishing, and disconnecting
    from an MQTT broker with structured error handling.
    """

    def __init__(self, host: str, port: int, user: str = None, password: str = None, timeout: int = 60):
        """
        Initialize MQTT client and establish connection

        :args:
            host:str - MQTT broker hostname or IP
            port:int - MQTT broker port
            user:str - optional username for authentication
            password:str - optional password for authentication
            timeout:int - keepalive timeout in seconds
        :params:
            self.client:mqtt.Client - underlying MQTT client instance
            self._connected:bool - connection state flag
        :return:
            None
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout

        self.client = mqtt.Client()
        self._connected = False

        # Register callback BEFORE connecting
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

        self.connect()

    # -------------------------
    # Callbacks
    # -------------------------

    def _on_connect(self, client, userdata, flags, rc):
        """
        Internal callback triggered upon connection attempt

        :args:
            client:mqtt.Client - MQTT client instance
            userdata:Any - user-defined data
            flags:dict - response flags from broker
            rc:int - result code
        :params:
            self._connected:bool - updated connection state
        :return:
            None
        """
        if rc == 0:
            self._connected = True
        else:
            error_msg = MQTT_ERROR_CODES.get(rc, f"Unknown error code {rc}")
            raise Exception(
                f"MQTT connection refused by {self.host}:{self.port} "
                f"(Error Code: {rc} - {error_msg})"
            )

    def _on_disconnect(self, client, userdata, rc):
        """
        Internal callback triggered upon disconnection

        :args:
            client:mqtt.Client - MQTT client instance
            userdata:Any - user-defined data
            rc:int - result code
        :params:
            self._connected:bool - updated connection state
        :return:
            None
        """
        self._connected = False
        if rc != 0:
            error_msg = MQTT_ERROR_CODES.get(rc, f"Unknown error code {rc}")
            raise Exception(
                f"Unexpected MQTT disconnection from {self.host}:{self.port} "
                f"(Error Code: {rc} - {error_msg})"
            )

    # -------------------------
    # Connection Handling
    # -------------------------

    def connect(self):
        """
        Establish connection to MQTT broker

        :args:
            None
        :params:
            self.client:mqtt.Client - configured client instance
            self._connected:bool - updated connection state
        :return:
            None
        """
        try:
            if self.user and self.password:
                self.client.username_pw_set(self.user, self.password)

            self.client.connect(self.host, self.port, keepalive=self.timeout)
            self.client.loop_start()

            # Wait for connection acknowledgement
            timeout_time = time.time() + 5
            while not self._connected:
                if time.time() > timeout_time:
                    raise TimeoutError(
                        f"MQTT connection timeout to {self.host}:{self.port}"
                    )
                time.sleep(0.05)

        except Exception as error:
            raise Exception(
                f"Failed to connect to MQTT broker {self.host}:{self.port} "
                f"(Error: {error})"
            )

    def disconnect(self):
        """
        Disconnect from MQTT broker

        :args:
            None
        :params:
            self.client:mqtt.Client - active MQTT client
        :return:
            None
        """
        try:
            if self.client.is_connected():
                self.client.loop_stop()
                self.client.disconnect()
        except Exception as error:
            raise Exception(
                f"Failed to disconnect from MQTT broker {self.host}:{self.port} "
                f"(Error: {error})"
            )

    # -------------------------
    # Publish
    # -------------------------

    def publish_data(self, topic: str, payload: str | dict | List[dict]):
        """
        Publish data to a specific MQTT topic

        :args:
            topic:str - MQTT topic name
            payload:str|dict|List[dict] - message content to publish
        :params:
            response:mqtt.MQTTMessageInfo - publish response object
            response.rc:int - MQTT return code
        :return:
            None
        """
        try:
            if not self._connected:
                raise Exception("MQTT client is not connected")

            if not isinstance(payload, (str, bytes, bytearray, int, float, type(None))):
                payload = json.dumps(payload)

            response = self.client.publish(topic, payload)

            # Wait for publish confirmation
            response.wait_for_publish()

            if response.rc != mqtt.MQTT_ERR_SUCCESS:
                error_msg = MQTT_ERROR_CODES.get(response.rc, "Unknown error")
                raise Exception(
                    f"Publish failed (Error Code: {response.rc} - {error_msg})"
                )

        except Exception as error:
            raise Exception(
                f"Failed to publish topic '{topic}' "
                f"against {self.host}:{self.port} (Error: {error})"
            )