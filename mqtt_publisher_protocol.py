# MQTT is lightweight IoT messaging protocol based on the publish/subscribe model, which can provide real-time and reliable messaging service for IoT devices. 
#
# Terminlogy 
#    * Subscriber: Edge device receiving data 
#    * Publisher: IoT device sending data 
#    * Broker: Host (IP) of the MQTT Subscriber 
#    * Topic: Type of information to subscribe to 
#    # Client ID: ID for openning connection 
# 
# The following code is based on: https://medium.com/@emqtt/how-to-use-mqtt-in-python-paho-4e622cb359f9

import random
import time
from paho.mqtt.client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

