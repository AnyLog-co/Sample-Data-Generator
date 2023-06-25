import argparse
import os
import random
import re
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
sys.path.insert(0, DATA_GENERATORS)

import data_generators.edgex_data as edgex_data
import publishing_protocols.publish_data as publish_data
from data_generators.file_processing import check_conversion_type


def __validate_conn_pattern(conns: str) -> str:
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

    for conn in conns.split(","):
        if not pattern1.match(conn) and not pattern2.match(conn):
            raise argparse.ArgumentTypeError(f'Invalid REST connection format: {conn}')

    return conns


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=__validate_conn_pattern, default=None,
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('protocol', type=str, choices=['post', 'mqtt', 'print', 'put', 'file'], default='post',
                        help='format to save data')
    parser.add_argument('--dir-name', type=str, default='$HOME/Downloads/sample_data/edgex-demo',
                        help='directory where files are stored - data is generated based on the file')
    parser.add_argument('--topic', type=str, default='edgex-video', help='topic to send data against')
    parser.add_argument('--db-name', type=str, default='edgex', help='Logical database to store data in')
    parser.add_argument('--table', type=str, default='videos', help='Logical database to store data in')
    parser.add_argument('--conversion-type', type=check_conversion_type, default='base64',
                        choices=['base64', 'bytesio', 'opencv'],
                        help='Format to convert file to - cv2 can be used for live camera feed')
    parser.add_argument('--qos', type=int, choices=list(range(0, 3)), default=0, help='MQTT Quality of Service')
    parser.add_argument('--repeat', type=int, default=1, help='Repeat process, if 0 run continuously')
    parser.add_argument('--sleep', type=float, default=10, help='Wait time between each insert')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether to print exceptions')
    args = parser.parse_args()
    repeat_count = 0
    payload = {
        "dbms": args.db_name,
        "table": args.table
    }
    if args.conn is not None:
        conns = args.conn.split(',')
        if args.protocol == "mqtt":
            conns = publish_data.connect_mqtt(conns, exception=args.exception)
            if not conns:
                print("Failed to set connection for MQTT publisher")
                exit(1)
        elif args.protocol in ["post", "put"]:
            conns = publish_data.setup_put_post_conn(conns=conns)
            if args.protocol == "put" and args.conversion_type != "bytesio":
                args.conversion_type = "bytesio" # must be bytesio for PUT


    while True:
        content = edgex_data.get_data(dir_path=args.dir_name, conversion_type=args.conversion_type, exception=args.exception)
        for key in content:
            payload[key] = content[key]

        publish_data.publish_data(payload=payload, insert_process=args.protocol, conns=conns, topic=args.topic,
                                  qos=args.qos, exception=args.exception)
        repeat_count += 1
        if repeat_count == args.repeat:
            exit(1)
        time.sleep(args.sleep)


if __name__ == '__main__':
    main()
