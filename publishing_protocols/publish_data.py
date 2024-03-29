import random

import generic_protocol
import mqtt_protocol
import rest_protocols
import support

def setup_put_post_conn(conns:list)->dict:
    """
    Convert connection information to dictionary format for PUT and POST commands
        {user}:{password}@{ip}:{port} --> {"{ip}:{port}" : ({user}, {password})
    :args:
        conns:list - list of connection information
    :params:
        connections:dict - converted conns
    :return:
        connections
    """
    connections = {}
    for conn in conns:
        ip_port = conn.split("@")[-1]
        connections[ip_port] = None
        if '@' in conn:
            connections[ip_port] = tuple(list(conn.split('@')[0].split(':')))

    return connections


def connect_mqtt(conns:list, exception:bool=False)->dict:
    """
    connect to MQTT client
    :args:
        conns:list - list of connections
        exception:bool - whether to print exceptions
    :params:
        mqtt_conns:dict - MQTT connections
        mqtt_conn:paho.mqtt.client.Client
    :return:
        mqtt_conns
    """
    mqtt_conns = {}
    user = None
    password = None
    for conn in conns:
        broker, port = conn.split("@")[-1].split(':')
        if '@' in conn:
            user, password = conn.split("@")[0].split(':')

        mqtt_conns[conn.split('@')[-1]] = {
            "user": user,
            "password": password
        }

    return mqtt_conns


def publish_data(payload, insert_process:str, conns:dict={}, topic:str=None, rest_timeout:int=30, qos:int=0, blob_data_type:str='',
                 conversion_type:str="base64", dir_name:str=None, compress:bool=False, last_conn:str=None, exception:bool=False):
    """
    Publish data based on the insert_process
    :args:
        payload - content to store either as a dict or list of dicts
        insert_process:str - format to store content in
        conn:str - connection information
        topic:str - REST POST + MQTT topic
        rest_timeout:int - REST timeout
        dir_name:str - directory to store files in
        compress:bool - whether to compress content or not when stored in file
        exception:bool - whether to print error message(s)
    :params:
        status:bool
    """
    conn = None
    auth = None

    if conns is not None:
        if len(conns) == 1:
            conn = list(conns)[0]
        else:
            # randomly select a connection to AnyLog, that has not been used the last time
            while conn == last_conn or conn is None:
                conn = random.choice(list(conns.keys()))
        if isinstance(conns, dict):
            auth = conns[conn]


    if conversion_type == 'bytesio' and blob_data_type == 'image' and insert_process != "file":
        payload['file_content'] = payload['file_content'].__str__()
    elif conversion_type == 'bytesio' and blob_data_type == 'video' and insert_process != "file":
        payload["readings"]["binaryValue"] = payload['file_content'].__str__()


    if insert_process == "print":
        str_payloads = support.json_dumps(payloads=payload)
        print(str_payloads)
    elif insert_process == "file" and blob_data_type == "":
        status = generic_protocol.write_to_file(payloads=payload, data_dir=dir_name, compress=compress,
                                                exception=exception)
    elif insert_process == "file" and blob_data_type != "":
        status = generic_protocol.write_blob_to_file(payloads=payload, data_dir=dir_name, blob_data_type=blob_data_type,
                                                     conversion_type=conversion_type, compress=compress,
                                                     exception=exception)
    elif insert_process == 'put':
        status = rest_protocols.put_data(payloads=payload, conn=conn, auth=auth, timeout=rest_timeout,
                                         exception=exception)
        if status is False and exception is False:
            print(f'Failed to insert one or more batches of data into {conn} via PUT')
    elif insert_process == 'post':
        status = rest_protocols.post_data(payloads=payload, topic=topic, conn=conn, auth=auth, timeout=rest_timeout,
                                          exception=exception)
        if status is False and exception is False:
            print(f'Failed to insert one or more batches of data into {conn} via POST')
    elif insert_process == 'mqtt':
        mqtt_protocol.mqtt_main(broker=conn.split(":")[0], port=conn.split(":")[-1], payloads=payload, topic=topic,
                                qos=qos, username=conns[conn]['user'], password=conns[conn]['password'],
                                exception=exception)

    return conn
