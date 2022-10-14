import argparse
import datetime
import os
import random
import sys
import uuid

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import video_image_processing
import support
import publish_data
import car_insight

PROCESS_ID = str(uuid.uuid4())
DEVICE_NAME='anylog-data-generator'
PROFILE_NAME='anylog-video-generator'


def main():
    """
    Main for processing files of vide or image type
    :positional arguments:
        file_name             file(s) to store in AnyLog. Use comma to send multiple files
    :optional arguments:
        -h, --help            show this help message and exit
        --device-name       DEVICE_NAME     name of device data is coming from
        --profile-name      PROFILE_NAME    name of device profile data is coming from
        --protocol          PROTOCOL        format to save data
            * file
            * (REST) POST
            * mqtt
            * kafka
        --conn              CONN            IP:Port credentials for either REST, MQTT or Kafka
        --topic             TOPIC           topic to send data agaisnt
        --dbms              DBMS            Logical database to store data in
        --table             TABLE           Logical database to store data in
        --authentication    AUTHENTICATION  username, password
        --timeout           TIMEOUT         REST timeout (in seconds)
        --compress          COMPRESS        Whether to compress create files, or decompress files being sent
        --exception         [EXCEPTION]     whether or not to print exceptions to screen

    :global:
        process_id:uuid.UUID - UUID for process
    :params:
       processed_data:dict - content in file converted to dictionary
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_name', type=str, default='$HOME/Downloads/videos', help='directory where files are stored')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('protocol', type=str, choices=['post', 'mqtt'], default='post', help='format to save data')
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
    list_dirs = os.listdir(dir_full_path)
    if args.reverse is True:
        list_dirs = list(reversed(list_dirs))

    conns = None
    conn = None
    conn_id = 0
    if args.conn is not None:
        conns = args.conn.split(',')


    for file_name in list_dirs:
        full_file_path =  os.path.join(dir_full_path, file_name)
        car_info = car_insight.car_counter()

        processed_data = video_image_processing.main(process_id=PROCESS_ID, file_name=full_file_path,
                                                     device_name=DEVICE_NAME, profile_name=PROFILE_NAME,
                                                     start_ts=car_info['start_ts'], end_ts=car_info['end_ts'],
                                                     speed=car_info['speed'], cars=car_info['cars'],
                                                     exception=args.exception)

        if conns is not None:
            conn = conns[conn_id]
            if conns is not None:
                conn_id += 1
                if conn_id == len(conns):
                    conn_id = 0
            publish_data.publish_data(payload=processed_data, insert_process='post', conn=conn,
                                      topic='anylogedgex-videos', rest_timeout=args.timeout, dir_name=None,
                                      compress=False, exception=True)
            exit(1)
        now = end_ts





if __name__ == '__main__':
    main()