import argparse
import cv2
import datetime
import numpy
import os
import random
import re
import time
import sys


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import publishing_protocols.publish_data as publish_data


def __validate_conn_pattern(conn:str)->str:
    """
    Validate connection information format is connect
    :valid formats:
        127.0.0.1:32049
        user:passwd@127.0.0.1:32049
    :args:
        conn:str - REST connection information
    :params:
        pattern1:str - compiled pattern 1 (127.0.0.1:32049)
        pattern2:str - compiled pattern 2 (user:passwd@127.0.0.1:32049)
    :return:
        if fails raises Error
        if success returns conn
    """
    pattern1 = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')
    pattern2 = re.compile(r'^\w+:\w+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')

    if not pattern1.match(conn) and not pattern2.match(conn):
        raise argparse.ArgumentTypeError(f'Invalid REST connection format: {conn}')

    return conn


def __row_size(arg):



def __take_photo(camera_id:int, exception:bool=False)->(numpy.ndarray):
    """
    Take a photo to be stored
    :args:
        camera_id:int - camera to take a photo with
        exception:bool - whether to print exceptions
    :params:
        cv2_content:cv2.VideoCapture - captured image
        frame:numpy.ndarry - captured photo as an array
    :return:
        frame
    """
    cv2_content = None
    frame = None

    try:
        cv2_content = cv2.VideoCapture(0)
    except Exception as error:
        if exception is True:
            print(f"Failed to take photo with camera ID {camera_id} (Error: {error})")


    if cv2_content is not None:
        try:
            _, frame = cv2_content.read()
        except Exception as error:
            if exception is True:
                print(f"Failed to read content for image (Error: {error})")

    return frame


def __create_payload(camera_id:int, db_name:str, table:str, frame:numpy.ndarray)->dict:
    """
    Create a payload for the given image
    :sample-payload:
        {
            "dbms": "test",
            "table": "live_feed",
            "camera": 0
            "ts": "2023-03-22T10:32:45.869737Z",
            "frame": [[0, 1, 0, 1], [1, 0, 0, 1]...],
            "value": 61.49,
            "units": "Celsius"
        }
    :args:
        frame:numpy.nddarry - image to be stored
    :params:
        timestamp:str - current timestamp in UTC
        payload:dict - content to be stored
    :return:
        payload
    """
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    payload = {
        "dbms": db_name,
        "table": table,
        "camera": camera_id,
        "ts": timestamp,
        "frame": frame,
        "value": round(random.randint(10, 90) + random.random(), 2),
        "unit": 'Celsius'
    }

    return payload


def main():
    """
    Data Generator for live camera feed
    :sample-policy:
    {"mapping": {
        "id": "livefeed",
        "dbms": "bring [dbms]",
        "table": "bring [table]",
        "timestamp": {
            "type": "timestamp",
            "bring": "[ts]"
        },
        "camera": {
            "type": "int",
            "bring": "[camera]"
        },
        "file": {
            "blob": true,
            "bring": "[frame]",
            "extension": "png",
            "apply": "opencv",
            "hash": "md5",
            "type": "varchar"
        },
        "value": {
            "type": "float",
            "bring": "[value]"
        },
        "unit": {
            "type": "string",
            "bring": "[unit]"
        }
    }}
    :positional arguments:
        camera_id             Camera ID to be used by cv2
        conn                  {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        protocol               format to save data
        * POST
        * MQTT
        * print
    :optional arguments:
        -h, --help                      show this help message and exit
        --topic         TOPIC           topic to send data agaisnt
        --db-name       DB_NAME         Logical database to store data in
        --table         TABLE           Logical database to store data in
        --sleep         SLEEP           Wait time between each file to insert
        --repeat        REPEAT          Number of times to repeat. If Set to 0, repeat indefinitly
        --timeout       TIMEOUT         REST timeout (in seconds)
        --exception     [EXCEPTION]     whether to print exceptions to screen
    :params:
        conns:dict - list of connect information
        frame:numpy.ndarray - frame as an array
        payload:dict - content to be stored
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('camera_id', type=int, default=0, help='Camera ID to be used by cv2')
    parser.add_argument('conn', type=__validate_conn_pattern, default='127.0.0.1:32149',
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('protocol', type=str, choices=['post', 'mqtt', 'print'], default='post',
                        help='format to save data')
    parser.add_argument('--topic', type=str, default='anylog-data-gen', help='topic to send data agaisnt')
    parser.add_argument('--qos', type=int, choices=list(range(0, 3)), default=0, help='MQTT Quality of Service')
    parser.add_argument('--db-name', type=str, default='edgex', help='Logical database to store data in')
    parser.add_argument('--table', type=str, default='image', help='Logical database to store data in')
    parser.add_argument('--sleep', type=float, default=5, help='Wait time between each file to insert')
    parser.add_argument('--repeat', type=__row_size, default=10, help='Number of times to repeat. If Set to 0, repeat indefinitly')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether to print exceptions to screen')
    args = parser.parse_args()

    conns = None
    if args.conn is not None:
        conns = args.conn.split(',')
        if args.protocol == "mqtt":
            conns = publish_data.connect_mqtt(conns, exception=args.exception)
            if not conns:
                print("Failed to set connection for MQTT publisher")
                exit(1)
        elif args.protocol in ["post", "put"]:
            conns = publish_data.setup_put_post_conn(conns=conns)

    if args.repeat > 0:
        for i in range(args.repeat):
            frame = __take_photo(camera_id=args.camera_id, exception=args.exception)
            if frame is not None:
                payload = __create_payload(camera_id=args.camera_id, db_name=args.db_name, table=args.table, frame=frame)
                publish_data.publish_data(payload=payload, insert_process=args.protocol, conns=conns, topic=args.topic,
                                          qos=args.qos, rest_timeout=args.timeout, dir_name=None, compress= False,
                                          exception=args.exception)
            time.sleep(args.sleep)
    else:
        while True:
            frame = __take_photo(camera_id=args.camera_id, exception=args.exception)
            if frame is not None:
                payload = __create_payload(camera_id=args.camera_id, db_name=args.db_name, table=args.table, frame=frame)
                publish_data.publish_data(payload=[payload], insert_process=args.protocol, conns=conns, topic=args.topic,
                                          qos=args.qos, rest_timeout=args.timeout, dir_name=None, compress=False,
                                          exception=args.exception)
            time.sleep(args.sleep)


if __name__ == '__main__':
    main()