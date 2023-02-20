
import paho.mqtt.client as mqtt
import os
import time

published_stat_ = False

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    global published_stat_
    print("mid: " + str(mid))
    published_stat_ = True

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)


def example():
    global published_stat_

    mqttc = mqtt.Client()
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Uncomment to enable debug messages
    #mqttc.on_log = on_log

    # Parse CLOUDMQTT_URL (or fallback to localhost)
    url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
    url = '10.0.0.78'
    port = 7850
    topic = "video-mapping"

    # Connect
    #mqttc.username_pw_set(url.username, url.password)
    mqttc.connect(url, port)

    # Start subscribe, with QoS level 0
    #mqttc.subscribe(topic, 0)

    # Publish a message
    mqttc.loop_start()


    published_stat_ = False
    mqttc.publish(topic, "my message"+ 4000 * '1')

    #time.sleep(5)
    # Continue the network loop, exit when an error occurs
    rc = 0



    published_stat_ = False
    mqttc.publish(topic, "my message"+ 4000 * '2')

    # Continue the network loop, exit when an error occurs
    # https://github.com/eclipse/paho.mqtt.python/blob/master/examples/publish_multiple.py

    rc = 0
    while not published_stat_:
          rc = mqttc.loop()
    print("rc: " + str(rc))


def main():
    example()
    '''
    print("\r\nConnect")
    client = connect_mqtt()

    print("\r\nPublish")
    publish(client)
    '''
'''
from paho.mqtt import client as mqtt_client
import time
import sys

# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

host  = '10.0.0.78'
port = 7850
topic = "video-mapping"
client_id = f'python-mqtt-1'
keepAlive = 300

run = True

def on_publish(client, userdata, mid):
    run = False;

def publish(client):
    global run
    msg_count = 0
    while True:
         time.sleep(1)
         msg = f"messages: {msg_count}" + 4000 * '1'
         result = client.publish(topic=topic, payload=msg, qos=0)
         client.loop()
         run = True;
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         msg_count += 1

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connect success!")
    else:
        print("connect failed...  error code is:" + str(rc))


def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        client.connect(host=host, port=port, keepalive=keepAlive)
    except:
        errno, value = sys.exc_info()[:2]
        print("MQTT publish failed with Error: (%s) %s" % (str(errno), str(value)))

    return client

'''

if __name__ == '__main__':
    main()