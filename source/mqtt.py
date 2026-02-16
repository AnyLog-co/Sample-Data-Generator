import json

import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, host:str, port:int, user:str=None, password:str=None, timeout:int=60):
        """
        method to publish data via MQTT
        :args:
            host:str - connection IP
            port:int - connection port
            user:str - connection user
            password:str - password associated with user
            sleep:float - wait time between each publish (group)
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout

        # super().__init__(host=host, port=port, user=user, password=password, timeout=timeout)
        self.client = mqtt.Client()

    def connect(self):
        """
        Connect to MQTT broker
        """
        try:
            if self.user and self.password:
                self.client.username_pw_set(username=self.user, password=self.password)
            self.client.connect(host=self.host, port=self.port, keepalive=self.timeout)
            self.client.loop_start()
        except Exception as error:
            raise Exception(f"Failed to connect to MQTT against {self.host}:{self.port} (Error: {error})")

    def disconnect(self):
        """
        Disconnect from MQTT broker
        """
        if self.client.is_connected():
            try:
                self.client.loop_stop()
                self.client.disconnect()
            except Exception as error:
                raise Exception(f"Failed to disconnect from MQTT against {self.host}:{self.port} (Error: {error})")

    def publish_data(self, topic:str, payload:str):
        """
        Publish content (payload) to a given topic
        :args:
            topic:str - topic to publish against
            payload:str - content to publish against topic
        :params:
            response:self.client.publish - response from MQTT publish request
        """
        if not self.client.is_connected():
            raise Exception(f"MQTT client is not connected")
        try:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            response = self.client.publish(topic, payload)
            response.wait_for_publish()
        except Exception as error:
            raise Exception(f"Failed to publish topic '{topic}' against {self.host}:{self.port} (Error: {error})")
