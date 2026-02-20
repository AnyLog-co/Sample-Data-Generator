import json
import time
import paho.mqtt.client as mqtt
from typing import List


class MqttClient:
    def __init__(self, host: str, port: int, user: str = None, password: str = None, timeout: int = 60):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout

        self.client = mqtt.Client()
        self._connected = False

        # Register callback
        self.connect()
        self.client.on_connect = self._on_connect

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._connected = True
        else:
            raise Exception(f"MQTT connection failed with rc={rc}")

    def connect(self):
        try:
            if self.user and self.password:
                self.client.username_pw_set(username=self.user, password=self.password)

            self.client.connect(self.host, self.port, keepalive=self.timeout)
            self.client.loop_start()

            # Wait for CONNACK
            timeout = time.time() + 5
            while not self._connected:
                if time.time() > timeout:
                    raise Exception(f"MQTT connection timeout to {self.host}:{self.port}")
                time.sleep(0.05)

        except Exception as error:
            raise Exception(f"Failed to connect to MQTT against {self.host}:{self.port} (Error: {error})")

    def disconnect(self):
        if self.client.is_connected():
            try:
                self.client.loop_stop()
                self.client.disconnect()
            except Exception as error:
                raise Exception(f"Failed to disconnect from MQTT against {self.host}:{self.port} (Error: {error})")

    def publish_data(self, topic: str, payload: str | dict | List[dict]):
        try:
            if not isinstance(payload, (str, bytearray, int, float, type(None))):
                payload = json.dumps(payload)

            response = self.client.publish(topic, payload)
            response.wait_for_publish()

        except Exception as error:
            raise Exception(
                f"Failed to publish topic '{topic}' against {self.host}:{self.port} (Error: {error})"
            )