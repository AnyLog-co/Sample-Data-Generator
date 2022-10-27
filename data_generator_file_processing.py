import argparse
import datetime
import os
import random
import sys
import time
import uuid

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import file_processing
import support
import publish_data
import car_insight

PROCESS_ID = str(uuid.uuid4())
DEVICE_NAME='anylog-data-generator'
PROFILE_NAME='anylog-video-generator'


def __create_data(process_id:str, file_name:str, binary_file:str, device_name:str="anylog-data-generator",
                  start_ts:str=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                  end_ts:str=(datetime.datetime.utcnow() + datetime.timedelta(seconds=5)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                  profile_name="anylog-video-generator", num_cars:int=0, speed:float=0)->dict:
    """
    Given the user information, create a JSON object
    :args:
        process_id:str - generated UUID process
        files_dict:dict - content to store
        device_name:str - name of device data is coming from
        profile_name:str - name of device profile data is coming from
    :params:
        data:dict - placeholder for JSON object to be stored in AnyLog
        file_name:str - file name without path
    :return:
        data
    :sample json:
    {
        "apiVersion": "v2",
        "id": "6b055b44-6eae-4f5d-b2fc-f9df19bf42cf",
        "deviceName": "anylog-data-generator",
        "origin": 1660163909,
        "profileName": "anylog-video-generator",
        "readings": [{
            "start_ts": "2022-01-01 00:00:00",
            "end_ts": "2022-01-01 00:00:05",
            "binaryValue": "AAAAHGZ0eXBtcDQyAAAAAWlzb21tcDQxbXA0MgADWChtb292AAAAbG12aGQAAAAA3xnEUt8ZxFMAAHUwAANvyQABAA",
            "mediaType": "video/mp4",
            "origin": 1660163909,
            "profileName": "traffic_data",
            "resourceName": "OnvifSnapshot",
            "valueType": "Binary",
            "num_cars": 5,
            "speed": 65.3
        }],
        "sourceName": "OnvifSnapshot"
    }
    """
    data = {
        "apiVersion": "v2",
        "id": process_id,
        "deviceName": device_name,
        "origin": int(time.time()),
        "profileName": profile_name,
        "readings": [],
        "sourceName": "OnvifSnapshot"
    }

    # file_name = file_name.
    data['readings'].append({
        "timestamp": start_ts,
        "start_ts": start_ts,
        "end_ts": end_ts,
        "binaryValue": binary_file,
        "deviceName": file_name.split('.')[0],
        "id": support.generate_string_hash(file_name=file_name, data=binary_file),
        "mediaType": support.media_type(file_suffix=file_name.rsplit('.', 1)[-1]),
        "origin": int(time.time()),
        "profileName": file_name.split('.')[1],
        "resourceName": "OnvifSnapshot",
        "valueType": "Binary",
        "num_cars": num_cars,
        "speed": speed
    })

    return data


def __publish_data(payload:dict, insert_process:str, conns:list, topic:str, rest_timeout:float, conn_id:int=0,
                   exception:bool=False)->int:
    """
    Publish data
    :args:
        payload:dict - content to store data
        insert_process:str - protocol to store data wih
        conns:list - list of connections
        topic:str - REST / MQTT topic
        rest_timeout:flloat - REST timeout
        conn_id:int - placeholder for current conn
        exception:bool - whether or not to print error message(s)
    :param:
        conn:str - current connection info
    :return:
        conn_id
    """
    if conns is not None:
        conn = conns[conn_id]
        conn_id += 1
        if conn_id == len(conns):
            conn_id = 0
    publish_data.publish_data(payload=payload, insert_process=insert_process, conn=conn, topic=topic,
                              rest_timeout=rest_timeout, dir_name=None, compress=False, exception=exception)
    return conn_id


def main():
    """
    Main for processing files of video or image and correlating it to a car speed & count row
    :positional arguments:
        dir_name              directory where files are stored
        conn                  {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        protocol              format to save data
            * post (default)
            * mqtt
            * print
    :optional arguments:
        -h, --help                      show this help message and exit
        --topic         TOPIC           topic to send data agaisnt
        --dbms          DBMS            Logical database to store data in
        --table         TABLE           Logical database to store data in
        --timeout       TIMEOUT         REST timeout (in seconds)
        --reverse       [REVERSE]       whether or not reverse order of files in directory
        --exception     [EXCEPTION]     whether or not to print exceptions to screen
    :global:
        process_id:uuid.UUID - UUID for process
    :params:
       processed_data:dict - content in file converted to dictionary
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_name', type=str, default='$HOME/Downloads/videos', help='directory where files are stored')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('protocol', type=str, choices=['post', 'mqtt', 'print'], default='post', help='format to save data')
    parser.add_argument('--topic',    type=str, default='anylog-data-gen', help='topic to send data agaisnt')
    parser.add_argument('--dbms',     type=str, default='edgex', help='Logical database to store data in')
    parser.add_argument('--table',    type=str, default='image', help='Logical database to store data in')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')
    parser.add_argument('--reverse', type=bool, nargs='?', const=True, default=False,
                        help='whether or not to print exceptions to screen')
    parser.add_argument('--exception', type=bool, nargs='?',     const=True, default=False,
                        help='whether or not to print exceptions to screen')
    args = parser.parse_args()

    dir_full_path = os.path.expandvars(os.path.expanduser(args.dir_name))
    conns = None
    conn_id = 0
    if args.conn is not None:
        conns = args.conn.split(',')

    if os.path.isdir(dir_full_path):
        payload = {}
        list_dirs = os.listdir(dir_full_path)
        if args.reverse is True:
            list_dirs = list(reversed(list_dirs))
        for file_name in list_dirs:
            payload = None
            full_file_path =  os.path.join(dir_full_path, file_name)
            car_info = car_insight.car_counter()

            # convert file content into binary-string
            file_content = file_processing.main(file_name=full_file_path, exception=args.exception)

            if file_content is not None:
                payload = create_data(process_id=PROCESS_ID, binary_file=file_content, file_name=file_name,
                                      device_name=DEVICE_NAME, profile_name=PROFILE_NAME,
                                      start_ts=car_info['start_ts'], end_ts=car_info['end_ts'],
                                      num_cars=car_info['cars'], speed=car_info['speed'])

            conn_id = __publish_data(payload=payload, insert_process=args.protocol, conns=conns, topic=args.topic,
                                     rest_time=args.timeout, conn_id=conn_id, exception=args.exception)
    elif os.path.isfile(dir_full_path):
        payload = {}
        file_content = file_processing.main(file_name=dir_full_path, exception=args.exception)
        car_info = car_insight.car_counter()
        if sys.platform.startswith('win'):
            file_name = dir_full_path.split('\\')[-1]
        else:
            file_name = dir_full_path.split('/')[-1]
        if file_content is not None:
            payload = create_data(process_id=PROCESS_ID, binary_file=file_content, file_name=file_name,
                                  device_name=DEVICE_NAME, profile_name=PROFILE_NAME,
                                  start_ts=car_info['start_ts'], end_ts=car_info['end_ts'],
                                  num_cars=car_info['cars'], speed=car_info['speed'])

        conn_id = __publish_data(payload=payload, insert_process=args.protocol, conns=conns, topic=args.topic,
                                 rest_time=args.timeout, conn_id=conn_id, exception=args.exception)


if __name__ == '__main__':
    main()