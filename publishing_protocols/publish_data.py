import random

import generic_protocol
import mqtt_protocol
import rest_protocols


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
        ip_port = conn.split("@")[-1].split(':')
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
        mqtt_conn = mqtt_protocol.connect_mqtt_broker(broker=broker, port=port, username=user, password=password, exception=exception)
        if mqtt_conn is not None:
            mqtt_conns[conn.split('@')[-1]] = mqtt_conn

    return mqtt_conns


def disconnect_mqtt(conns:dict, exception:bool=False):
    """
    Disconnect from MQTT client
    :args:
        conns:dict - MQTT connection information
        exception:bool - whether to print exceptions
    """
    for conn in conns:
        mqtt_protocol.disconnect_mqtt(conn_info=conn, mqtt_conn=conns[conn], exception=exception)


def publish_data(payload, insert_process:str, conns:dict={}, topic:str=None, rest_timeout:int=30, blob_data_type:str='',
                 conversion_type:str="base64", dir_name:str=None, compress:bool=False, exception:bool=False):
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
    mqtt_conn = None
    if conns:
        conn = random.choice(list(conns.keys()))
    if insert_process in ['put', 'post']:
        auth = conns[conn]
    elif insert_process == "mqtt":
        mqtt_conn = conns[conn]

    if insert_process == "print":
        generic_protocol.print_content(payloads=payload, conversion_type=conversion_type)

    # elif insert_process == "file":
    #     blob = ''
    #     if blob_data_type == 'image':
    #         blob = payload["file_content"]
    #         del payload["file_content"]
    #     elif blob_data_type == 'video':
    #         blob = payload["readings"]["binaryValue"]
    #         del payload["readings"]["binaryValue"]
    #
    #     status = generic_protocol.write_to_file(payloads=payload, blob=blob, data_dir=dir_name, conversion_type=conversion_type,
    #                                             compress=compress, exception=exception)

        # if status is False and exception is False:
        #     print(f'Failed to store content into file')
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
        status = mqtt_protocol.mqtt_process(mqtt_client=mqtt_conn, payloads=payload, topic=topic, exception=exception)
        if status is False and exception is False:
            print(f'Failed to send MQTT message against connection {conn}')
        else:
            print('success')

