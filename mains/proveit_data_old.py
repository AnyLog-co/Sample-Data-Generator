import asyncio
import os
import json
import time

from source.opcua import OpcuaServer
from source.mqtt import MqttClient
from source.support import read_chunks


# Get Directory
DATA_DIR = os.path.join(os.path.dirname(__file__).split("mains")[0], "data", "proveit-data")
if not DATA_DIR:
    raise NotADirectoryError(f"Failed to locate directory {DATA_DIR}")

# Get Files in directory
FILES = os.listdir(DATA_DIR)
if not FILES:
    raise FileNotFoundError(f"Failed to locate file(s) in {DATA_DIR}")

def proveit(client:(OpcuaServer or MqttClient)):
    while True:
        for fname in FILES:
            try:
                with open(os.path.join(DATA_DIR, fname)) as f:
                    for batch in read_chunks(f, 100):
                        for row in batch:
                            row = row.strip()
                            if not row:
                                continue

                            data = json.loads(row)
                            topic = data.get("topic")
                            payload = data.get("msg")

                            if topic:
                                if isinstance(client, OpcuaServer):
                                    asyncio.run(client.publish_data(topic, payload))
                                else:
                                    client.publish_data(topic, payload)
                            time.sleep(0.5)

            except Exception as error:
                raise Exception(f"Failed to publish data from {fname} against {'MQTT' if isinstance(client, MqttClient) else 'OPC-UA'} (Error: {error})")

