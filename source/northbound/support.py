"""
Support for northbound services - where to publish data based on user definiton
"""
import asyncio
import json

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt import MqttClient
from source.northbound.kafka import KafkaClient
from source.northbound.opcua import OpcuaServer


def _publish_data(method:str, conn:MqttClient|RestClient|OpcuaServer|KafkaClient, payload,
                  topic:str=None, headers:dict=None, loop=None):
    """
    Publishing data process for situations where the information is topic based - extension of `publish_data` function
    """
    if method in ["MQTT", "KAFKA"]:
        conn.publish_data(topic=topic, payload=payload)
    elif method == "POST":
        headers.update({
            "command": "data",
            "topic": topic
        })
        headers["Content-Type"] = "application/json"
        conn.publish_data(headers=headers, payload=payload, method=method)
    elif method == "OPCUA":
        try:
            if isinstance(payload, list):
                for idx in range(len(payload)):
                    future = asyncio.run_coroutine_threadsafe(
                        conn.publish_data(topic=f"{topic}/{idx}", payload=payload[idx]), loop
                    )
            else:
                future = asyncio.run_coroutine_threadsafe(
                    conn.publish_data(topic=topic, payload=payload), loop
                )
        except Exception as error:
            raise Exception(f"Failed to define OPC-UA loop (Error: {error})")
        else:
            future.result()


def publish_data(method:str, conn:MqttClient|RestClient|OpcuaServer|KafkaClient, payload,  topic:str=None,
                 table_name:str=None, db_name:str=None, idx:int|None=None, standalone_values:bool=False, loop=None):
    """
    main for publishing data
    :args:
        method:str - method to publish data
        conn:MqttClient|RestClient - logic to publish with
        payload - content to publish
        topic:str - for MQTT / POST topic to publish against
        table_name:str - for PUT logical table name
        db_name:str - for PUT logical table name
        standalone_values:bool - when inserting data via POST, MQTT, Kafka or OPC-UA each key/value pair will have its
        own topic
    :params:
        headers:dict - REST headers for when publishing via POST or PUT
    """
    headers = {
        "User-Agent": "AnyLog/1.23",
        "Content-Type": "text/plain"
    }

    if method == "PRINT":
        topic = f"{topic} - " if topic else ""
        print(f"{topic}{json.dumps(payload, indent=2)}")
        exit(1)
    elif method == "PUT":
        headers.update({
            "type": "json",
            "dbms": db_name,
            "table": table_name,
            "mode": "streaming"
        })
        conn.publish_data(headers=headers, payload=payload, method=method)
    elif standalone_values and method in ["MQTT", "KAFKA", "POST", "OPCUA"] and isinstance(payload, list):
        for idx in range(len(payload)):
            publish_data(method=method, conn=conn, topic=topic, payload=payload[idx], idx=idx,
                         db_name=db_name, table_name=table_name, standalone_values=standalone_values, loop=loop)
    elif standalone_values and method in ["MQTT", "KAFKA", "POST", "OPCUA"] and isinstance(payload, dict):
        for key, value in payload.items():
            key = f"{idx}/{key}" if key and (idx is not None and idx >= 0) else key
            _publish_data(method=method, conn=conn, topic=f"{topic}/{key}", payload=value, headers=headers, loop=loop)
    elif method in ["MQTT", "KAFKA", "POST", "OPCUA"]:
        _publish_data(method=method, conn=conn, topic=topic, payload=payload, headers=headers, loop=loop)

    else:
        raise Exception(f"Invalid publish type {method}")


def configure_connection(method:str, conn:str, timeout:float=30):
    auth = ()
    if '@' in auth:
        auth, conn = conn.split('@')
        auth = tuple(auth.split(':'))
    host, port = conn.split(':')

    if method in ["POST", "PUT"]:
        conn = RestClient(conn=conn, auth=auth, timeout=timeout)
    elif method in ["MQTT", "KAFKA"] :
        FNC = MqttClient if method == "MQTT" else KafkaClient
        user = None
        password = None
        if auth:
            user, password = auth
        conn = FNC(host=host, port=int(port), user=user, password=password)

    return conn

