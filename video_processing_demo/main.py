import argparse
import datetime
import os
import sys
import uuid

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split('video_processing_demo')[0]
PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, PROTOCOLS)

import file_processing
import support
import publish_data

DATA_DIR = os.path.join(ROOT_PATH, 'data')

def main():
    """
    The following demo demonstrate processing files into AnyLog and associating them with a SQL consisting of
   start_time, end_time and number of cars & (avg) car speed
    :positional arguments:
        dir_name              directory containing videos and/or images to be processed
        insert_process        format to store generated data
            * print
            * file
            * put
            * post
            * mqtt
        db_name               logical database name
    :optional arguments:
        -h, --help                      show this help message and exit
        --batch-size    BATCH_SIZE      number of rows to insert per iteration
        --process-id    PROCESS_ID      UUID Process ID - default changes each iteration
        --device_name   DEVICE_NAME     name of device data is coming from
        --profile_name  PROFILE_NAME    name of device profile data is coming from
        --reverse       [REVERSE]       reverse file order in video/image directory
        --conn          CONN            {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        --topic         TOPIC           topic for publishing data via REST POST or MQTT
        --rest-timeout  REST_TIMEOUT    how long to wait before stopping REST
        --archive-dir   ARCHIVE_DIR     directory when storing to file
        --compress      [COMPRESS]      whether to zip data dir
        --exception     [EXCEPTION]     whether to print exceptions
    :params:
        status:bool
        dir_name:str - directory containing image/video files
        list_dir:list - files within dir_name
        speed:float - "car" speed
        cars:int - number of "cars"
        binary_file:str - file content as binary string (base64)
        payload:dict - content to store in AnyLog
    """
    parse = argparse.ArgumentParser()
    parse.add_argument('dir_name', type=str, default='$HOME/Sample-Data-Generator/data/videos',
                        help='directory containing videos and/or images to be processed')
    parse.add_argument('insert_process', type=str, choices=['print', 'file', 'put', 'post', 'mqtt'],
                       default='print', help='format to store generated data')
    parse.add_argument('db_name', type=str, default='test', help='logical database name')
    parse.add_argument('--batch-size', type=int, default=5, help='number of rows to insert per iteration')
    parse.add_argument('--process-id', type=str, default=str(uuid.uuid4()),
                        help='UUID Process ID - default changes each iteration')
    parse.add_argument('--device_name', type=str, default='anylog-data-generator',
                        help='name of device data is coming from')
    parse.add_argument('--profile_name', type=str, default='anylog-video-generator',
                        help='name of device profile data is coming from')
    parse.add_argument('--reverse', type=bool, nargs='?', const=True, default=False,
                        help='reverse file order in video/image directory')
    parse.add_argument('--conn', type=str, default=None,
                       help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parse.add_argument('--topic', type=str, default=None, help='topic for publishing data via REST POST or MQTT')
    parse.add_argument('--rest-timeout', type=float, default=30, help='how long to wait before stopping REST')
    parse.add_argument('--archive-dir', type=str, default=DATA_DIR, help='directory when storing to file')
    parse.add_argument('--compress', type=bool, nargs='?', const=True, default=False, help='whether to zip data dir')
    parse.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                       help='whether to print exceptions')
    args = parse.parse_args()

    payloads = []

    dir_name = os.path.expandvars(os.path.expanduser(args.dir_name))
    list_dir = []
    if not os.path.isdir(dir_name):
        print(f'Failed to locate {dir_name}. Cannot continue')
        exit(1)
    else:
        list_dir = os.listdir(dir_name)
        if args.reverse is True:
            list_dir.reverse()

    for file_name in list_dir:
        start_ts, end_ts = support.generate_timestamp(now=now)
        speed, cars = support.car_counter(timestamp=start_ts)

        # read content in file & store in 64 bytes
        full_name = os.path.join(dir_name, file_name)
        status, binary_file = file_proceessing.image_processing(file_name=full_name, exception=args.exception)


        if status is True and not isinstance(binary_file, None):
            payload = support.create_data(process_id=args.process_id, file_name=file_name, binary_file=binary_file,
                                          device_name=ars.device_name, start_ts=start_ts, end_ts=start_ts,
                                          profile_name=args.profile_name, num_car=cars, speed=speed, 
                                          db_name=args.db_name)
            payloads.append(payload)

        if len(payloads) == args.batch_size: # publish data
            publish_data.publish_data(payload=payloads, insert_process=args.insert_process, conn=conn,
                                      compress=args.compress, rest_timeout=args.rest_timeout, dir_name=args.archive_dir)
    if len(payloads) > 0: # publish data
        publish_data.publish_data(payload=payloads, insert_process=args.insert_process, conn=conn,
                                  compress=args.compress, rest_timeout=args.rest_timeout, dir_name=args.archive_dir)


if __name__ == '__main__':
    main()
