import asyncio
import json
from typing import List

from source.northbound.mqtt_calls import MqttClient
from source.northbound.rest_calls import RestClient
from source.northbound.opcua import OpcuaServer

def publish_data(method:str, conn:MqttClient|RestClient|OpcuaServer, payload:dict|List[dict],  topic:str=None, table_name:str=None,
                 db_name:str=None):
    """
    main for publishing data
    :args:
        method:str - method to publish data
        conn:MqttClient|RestClient - logic to publish with
        payload:dict|List[dict] - content to publish
        topic:str - for MQTT / POST topic to publish against
        table_name:str - for PUT logical table name
        db_name:str - for PUT logical table name
    :params:
        headers:dict - REST headers for when publishing via POST or PUT
    """
    headers = {
        "User-Agent": "AnyLog/1.23",
        "Content-Type": "text/plain"
    }

    if method == "PRINT":
        print(json.dumps(payload, indent=2))
    if method == "MQTT":
        conn.publish_data(topic=topic, payload=payload)
    elif method == "PUT":
        headers.update({
            "type": "json",
            "dbms": db_name,
            "table": table_name,
            "mode": "streaming"
        })
        conn.publish_data(headers=headers, payload=payload, method=method)
    elif method == "POST":
        headers.update({
            "command": "data",
            "topic": topic
        })
        conn.publish_data(headers=headers, payload=payload, method=method)
