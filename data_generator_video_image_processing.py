import argparse
import datetime
import os
import random
import sys
import uuid

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PROTOCOLS)

import video_image_processing
import publish_data
import support

PROCESS_ID = str(uuid.uuid4())


DIR_NAME='$HOME/Downloads/videos'
DEVICE_NAME='anylog-data-generator'
PROFILE_NAME='anylog-video-generator'

def __generate_timestamp(now:datetime.datetime)->(datetime.datetime, datetime.datetime):
    """
    Given current timestamp, generate start/end time(s)
    :args:
        now:datetime.datetime - base timestamp
    :params:
        start:datetime.datetime - "starting" timestamp
        end:datetime.datetime - "ending" timestamp
    :return:
        start, end
    """
    start = now + datetime.timedelta(hours=int(random.random() * 5))
    end = start + datetime.timedelta(seconds=30, microseconds=random.choice(range(0, 999999)))
    return start, end


def __car_counter(timestamp:datetime.datetime)->(int, float):
    """
    Generate (avg) cars speed + number of cars
    :args:
        timestamp:datetime.datetime - timestamp to be used for calculations
    :params:
        hours:int - from timestamp extract hour value
        speed:float - "avg" car speed
        cars:int - number of cars on the road
    :return:
        cars, speed
    """
    hours = timestamp.hour

    if 5 <= hours < 7:
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
        cars = int(random.choice(range(10, 30)))
    elif 7 <= hours < 10:
        speed = round(random.choice(range(45, 65)) - random.random(), 2)
        cars = int(random.choice(range(40, 60)))
    elif 10 <= hours < 16:
        cars = int(random.choice(range(5, 20)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
    elif 16 <= hours < 20:
        speed = round(random.choice(range(45, 65)) - random.random(), 2)
        cars = int(random.choice(range(40, 60)))
    elif 20 <= hours < 23:
        cars = int(random.choice(range(5, 20)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
    else: # 23:00 to 5:00
        cars = int(random.choice(range(0, 15)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
        if cars == 0:
            speed = 0

    return speed, cars



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

    # sending params
    parser.add_argument('--protocol', type=str, choices=['post', 'mqtt', 'kafka', 'file'], default='file', help='format to save data')
    parser.add_argument('--conn',     type=str, default='127.0.0.1:2049', help='IP:Port credentials for either REST, MQTT or Kafka')
    parser.add_argument('--topic',    type=str, default='anylog-data-gen', help='topic to send data agaisnt')
    parser.add_argument('--dbms',     type=str, default='edgex', help='Logical database to store data in')
    parser.add_argument('--table',    type=str, default='image', help='Logical database to store data in')
    parser.add_argument('--authentication', type=str, default=None, help='username, password')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')

    # other
    parser.add_argument('--compress', type=bool, nargs='?', const=True, default=False, help='Whether to compress create files, or decompress files being sent')
    parser.add_argument('--exception', type=bool, nargs='?',     const=True, default=False, help='whether or not to print exceptions to screen')
    args = parser.parse_args()

    dirs_full_path = os.path.expandvars(os.path.expanduser(DIR_NAME))
    if not os.path.isdir(dirs_full_path):
        print(f'Failed to locate directory {DIR_NAME}, cannot continue')
        exit(1)
    list_dirs = os.listdir(dirs_full_path)
    reversed_list_dirs = list(reversed(list_dirs))
    now = datetime.datetime.strptime('2022-07-30T00:00:00.000000Z', '%Y-%m-%dT%H:%M:%S.%fZ')

    for file_name in list_dirs:
        index = list_dirs.index(file_name)
        last_file = reversed_list_dirs[index]
        file_name = os.path.join(dirs_full_path, file_name)

        start_ts, end_ts = __generate_timestamp(now=now)
        for conn in args.conn.split(','):
            speed, cars = __car_counter(timestamp=start_ts)
            print(conn, index)
            if conn == args.conn.split(',')[-1]:
                file_name = os.path.join(dirs_full_path, last_file)
            processed_data=video_image_processing.main(process_id=PROCESS_ID, file_name=file_name,
                                                       device_name=DEVICE_NAME, profile_name=PROFILE_NAME,
                                                       start_ts=start_ts, end_ts=end_ts, speed=speed, cars=cars,
                                                       exception=args.exception)
            publish_data.publish_data(payload=processed_data, insert_process=args.protocol, conn=conn, topic=args.topic,
                                      compress=True, rest_timeout=30, exception=args.exception)
        now = end_ts


    # end_ts = args.end_ts
    # file_list = args.file_name.split(',')
    # conns_list = args.conn.split(',')
    # conn = conns_list[0]
    # for file_name in file_list:
    #     if len(conns_list) == len(file_list)
    #         conn = conns_list[file_list.index(file_name)]


if __name__ == '__main__':
    main()