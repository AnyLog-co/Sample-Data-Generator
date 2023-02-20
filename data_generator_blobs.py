import argparse
import importlib
import os
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
sys.path.insert(0, DATA_GENERATORS)

import data_generators.data_generator_images as data_generator_images
import data_generators.data_generator_videos as data_generator_videos
import publishing_protocols.publish_data as publish_data
from data_generators.file_processing import check_conversion_type

def main():
    """
    The following provides an example for storing blobs (ex. images and videos) with associated values into AnyLog.
    The data set for this data generator can be downloaded here: https://drive.google.com/drive/folders/1EuArx1VepoLj3CXGrCRcxzWZyurgUO3u?usp=share_link
    :note:
        on the AnyLog side, make sure MongoDB is running and associated `run mqtt client` is active. Otherwise, data
        will not come in and/or will not be stored
    :positional arguments:
        dir_name    directory where files are stored
        conn        {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        protocol    format to save data
            * post
            * mqtt
            * print
    :options:
        -h, --help                show this help message and exit
        --topic     TOPIC         topic to send data agaisnt
        --table     TABLE         Logical database to store data in
        --sleep     SLEEP         Wait time between each file to insert
        --timeout   TIMEOUT       REST timeout (in seconds)
        --timezone  TIMEZONE      timezone for generated timestamp(s)
            * local
            * utc
            * et
            * br
            * jp
            * ws
            * au
            * it
        --enable-timezone-range     [ENABLE_TIMEZONE_RANGE]     set timestamp within a range of +/- 1 month
        --conversion-type           CONVERSION_TYPE             Format to convert file to - cv2 can be used for live camera feed
            * base64
            * bytesio
            * cv2
        --reverse                   [REVERSE]                   whether to store data in reversed (file) order
        --exception                 [EXCEPTION]                 whether to print exceptions to screen
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_name', type=str, default='$HOME/Downloads/sample_data/videos',
                        help='directory where files are stored - data is generated based on the file')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('protocol', type=check_conversion_type, choices=['post', 'mqtt', 'print', 'put'], default='post',
                        help='format to save data')
    parser.add_argument('--topic', type=str, default='anylog-data-gen', help='topic to send data agaisnt')
    parser.add_argument('--db-name', type=str, default='edgex', help='Logical database to store data in')
    parser.add_argument('--table', type=str, default='image', help='Logical database to store data in')
    parser.add_argument('--sleep', type=float, default=5, help='Wait time between each file to insert')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')
    parser.add_argument('--timezone', type=str, choices=['local', 'utc', 'et', 'br', 'jp', 'ws', 'au', 'it'],
                        default='local', help='timezone for generated timestamp(s)')
    parser.add_argument('--enable-timezone-range', type=bool, nargs='?', const=True, default=False,
                        help='set timestamp within a range of +/- 1 month')
    parser.add_argument('--conversion-type', type=str, default='base64', choices=['base64', 'bytesio', 'cv2'],
                        help='Format to convert file to - cv2 can be used for live camera feed')
    parser.add_argument('--reverse', type=bool, nargs='?', const=True, default=False,
                        help='whether to store data in reversed (file) order')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether to print exceptions to screen')
    args = parser.parse_args()

    # validate directory exists
    args.dir_name = os.path.expanduser(os.path.expandvars(args.dir_name))
    if not os.path.isdir(args.dir_name):
        print(f"Failed to locate data directory {args.dir_name}, cannot continue...")
        exit(1)

    if __check_conversion_type(conversion_type=args.conversion_type) is False:
        exit(1)

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

    if 'win32' in sys.platform and args.dir_name[-1] == '\\':
        sub_dir = args.dir_name[:-1].rsplit('\\')[-1]
    elif 'win32' in sys.platform:
        sub_dir = args.dir_name.rsplit('\\')[-1]
    elif args.dir_name[-1] == '/':
        sub_dir = args.dir_name[:-1].rsplit('/')[-1]
    else:
        sub_dir = args.dir_name.rsplit('/')[-1]

    if sub_dir == "videos":
        data_generator_videos.main(dir_name=args.dir_name, conns=conns, protocol=args.protocol, topic=args.topic,
                                   db_name=args.db_name, table=args.table, sleep=args.sleep, timezone=args.timezone,
                                   timeout=args.timeout, enable_timezone_range=args.enable_timezone_range,
                                   reverse=args.reverse, conversion_type=args.conversion_type, exception=args.exception)
    if sub_dir == "images":
        data_generator_images.main(dir_name=args.dir_name, conns=conns, protocol=args.protocol, topic=args.topic,
                                   db_name=args.db_name, table=args.table, sleep=args.sleep, timeout=args.timeout,
                                   reverse=args.reverse, conversion_type=args.conversion_type, exception=args.exception)

    if args.protocol == "mqtt":
        publish_data.disconnect_mqtt(conns=conns, exception=args.exception)


if __name__ == '__main__':
    main()
