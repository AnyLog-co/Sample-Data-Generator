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

def get_file_content(url:str=None, timeout:float=30):
    """
    Given a URL, extract content from.
    :use-cases:
        1. get list of files
        2. read content from file
    :args:
        url:str - URL to extract content from
        timeout:float - REST timeout
    :params:
        temp_conn:RestClient - Connection to URL
    :return:
        raw response

    """
    temp_conn = RestClient(conn=url, auth=(), timeout=timeout)
    return temp_conn.get_data(headers=None, raw_response=True)

def declare_mapping_policy(conn:RestClient, policy:dict, **kwargs)->str|None:
    #--- To review ---#
    """
    Check whether a policy exists and if not declare policy and extract policy ID
    can be used for
        - mapping
        - uns
    :args:
        conn:RestClient - connection to REST
        policy:dict - Policy to publish
        kwargs:dict - arguments for WHERE when checking if policy exists
    :params:
        policy_id:str - extract policy ID if exists
    """
    try:
        policy_id = policy.get("mapping").get("id")
    except AttributeError:
        policy_id = None

    get_headers = {
        "command": f"blockchain get *",
        "User-Agent": "AnyLog/1.23"
    }

    if policy_id or kwargs:
        get_headers["command"] += " where "
        if policy_id and "id" not in list(kwargs.values()):
            get_headers["command"] += f' id="{policy_id}" and '
        for name, var in kwargs.items():
            get_headers["command"] += f'{name}="{var}" and '
        get_headers["command"] = get_headers["command"].rsplit(" and ", 1)[0]
    get_headers["command"] += " bring [*][id]"

    publish_headers = {
        "command": "blockchain insert where policy=!new_policy and local=true and master=!ledger_conn",
        "User-Agent": "Anylog/1.23"
    }

    response = conn.get_data(headers=get_headers)
    index = 0
    while not response or response == "[]":
        if index > 0:
            raise ConnectionError(f"Failed to publish policy against {conn.url}")
        new_policy = f"<new_policy={json.dumps(policy)}>"
        conn.publish_data(headers=publish_headers, payload=new_policy, method="POST")
        response = conn.get_data(headers=get_headers)
        index += 1

    return response


def declare_msg_client(conn:RestClient, broker:str, port:int, topics:str|list, is_rest:bool=True):
    # --- To review ---#
    is_topics = False
    if not isinstance(topics, list):
        topics = topics.split(',')

    for topic in topics:
        msg_topic = topic.split('name=', 1)[-1].split('and', 1)[0].strip()
        check_msg_client = {
            "command": f"get msg client where topic={msg_topic}",
            "User-Agent": "AnyLog/1.23"
        }
        response = conn.get_data(headers=check_msg_client)
        if not (response.strip() in ["No message client subscriptions", "No such client subscription"]):
            is_topics = True
            if len(topics) > 1:
                print(f"Topic {msg_topic} already defined, cannot define `msg client` for provided topics")

    if not is_topics:
        declare_msg_client_header = {
            "command": f"run msg client where broker={broker} and log=false",
            "User-Agent": "AnyLog/1.23"
        }
        for topic in topics:
            declare_msg_client_header["command"] += f" and topic={topic}"


        if broker not in ["rest", "local"] and port:
            declare_msg_client_header["command"] += f" and port={port}"
        if broker  == "rest" or is_rest is True:
            declare_msg_client_header["command"] += f" and user-agent=anylog"

        conn.publish_data(headers=declare_msg_client_header, payload=None, method="POST")