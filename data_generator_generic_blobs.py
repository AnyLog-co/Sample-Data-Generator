import argparse
import json
import os
import random
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import data_generators.data_generator_images as data_generator_images
import data_generators.data_generator_videos as data_generator_videos
import data_generators.edgex_data as edgex_data
import publishing_protocols.publish_data as publish_data
import publishing_protocols.support as support

DATA_DIR = os.path.join(ROOT_PATH, 'data', "new-data")
MICROSECONDS = random.choice(range(100, 300000)) # initial microseconds for timestamp value
SECOND_INCREMENTS = 86400  # second increments (0.864) for 100000 rows

class ExtendedHelpAction(argparse.Action):
    def __rows_summary(self, db_name:str='test')->str:
        """
        The following provides an example for each of the data types, printing them to screen
        :args:
            db_name:str - logical database name
        :params:
            payloads:dict - sample data
        """
        payloads = {
            'edgex': {
                "dbms": db_name,
                "table": "people_video",
                "start_ts": "2023-07-11T23:36:31.428555",
                "end_ts": "2023-07-11T23:36:36.428569",
                "file_content": "AAAAIGZ0eXBpc29tAAAC...",
                "count": 4,
                "confidence": 0.75
            },
            'image': {
                "id": "57195181-21b1-4a1b-b21e-293783a267e4",
                "dbms": db_name,
                "table": "images",
                "file_name": "20200306202534601.jpeg",
                "file_type": "image/jpeg",
                "file_content": "/9j/4AAQSkZJRgABAQAA...",
                "detection": [{
                    "class": "kizu",
                    "bbox": [658, 657, 674, 671],
                    "score": 0.59605
                }],
                "status": "ok"
            },
            'video': {
                "apiVersion": "v2",
                "dbName": db_name,
                "id": "856e7dd0-ea63-4a8d-9f57-ba9f578c6fd2",
                "deviceName": "videos",
                "origin": 1689121459,
                "profileName": "anylog-video-generator",
                "readings": [{
                    "timestamp": "2023-07-11T17:24:19.120476Z",
                    "start_ts": "2023-07-11T17:24:19.120476Z",
                    "end_ts": "2023-07-11T17:25:44.120476Z",
                    "binaryValue": "AAAAIGZ0eXBpc29tAAAC...",
                    "deviceName": "video18A",
                    "id": "27618fc9-3df9-ee59-46e7-11748debdbe5",
                    "mediaType": "video/mp4",
                    "origin": 1689121459,
                    "profileName": "mp4",
                    "resourceName": "OnvifSnapshot",
                    "valueType": "Binary",
                    "num_cars": 40,
                    "speed": 59.79
                }],
                "sourceName": "OnvifSnapshot"
            }
        }

        for table in payloads:
            print(f'Data Type: {table}')
            if isinstance(payloads[table], list):
                for payload in payloads[table]:
                    print(f"\t{json.dumps(payload, indent=None)}")
            else:
                print(f"\t{json.dumps(payloads[table], indent=None)}")
        print("\n")

    def __call__(self, parser, namespace, values, option_string=None):
        # Call your function to handle extended help here
        print("Sample Data Types Available")
        self.__rows_summary(db_name='test')
        setattr(namespace, self.dest, True)
        print("""Sample docker call: \ndocker run -it --detach-keys=ctrl-d --name blobs-data-generator --network host \\
                    \t-e DATA_TYPE=edgex \\
                    \t-e INSERT_PROCESS=mqtt \\
                    \t-e DB_NAME=test \\
                    \t-e TOTAL_ROWS=100 \\
                    \t-e BATCH_SIZE=10 \\
                    \t-e SLEEP=0.5 \\
                    \t-e CONN=198.74.50.131:32149,178.79.143.174:32149 \\
                    \t-e TIMEZONE=utc \\
                    \t--rm anylogco/blobs-data-generator:latest\n""")
        exit(1)


def __data_types(value:str)->str:
    """
    Validate data types
    :args:
        value:str - user inputted data type(s)
    :return:
        value
        if fails error
    """
    if value not in ['edgex', 'video', 'image']:
        argparse.ArgumentError(f"Unsupported data type: {value}. Supported data types: edgex, video, image")
    return value


def __insert_process(value:str)->str:
    """
    Validate insert process
    :args:
        value:str - user inputted process type
    :return:
        value
        if fails error
    """
    if value not in ['print', 'post', 'mqtt']:
        argparse.ArgumentError(f"Unsupported process type: {value}. Supported process types: print, post, mqtt")
    return value


def main():
    """
    Data generator for videos and images
    :positional arguments:
        data_type             type of data to insert into AnyLog.
            * edgex
            * image
            * video
        insert_process        format to store generated data.
            * print
            * post
            * mqtt
        db_name               logical database name
    :optional arguments:
        -h, --help                              show this help message and exit
        --extended-help     [EXTENDED_HELP]     Generates help, but extends to include a sample row per data type
        --conversion-type   CONVERSION_TYPE     Format to convert content to be stored in AnyLog.
            * base64
            * bytesio
            * opencv
        --table-name        TABLE_NAME          Change default table name
        --total-rows        TOTAL_ROWS          number of rows to insert. If set to 0, will run continuously
        --batch-size        BATCH_SIZE          number of rows to insert per iteration
        --sleep             SLEEP               wait time between each row
        --timezone          TIMEZONE            timezone for generated timestamp(s)
            * local
            * utc
            * et
            * br
            * jp
            * ws
            * au
            * it
        --enable-timezone-range     [ENABLE_TIMEZONE_RANGE]     set timestamp within a range of +/- 1 month
        --conn      CONN        {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        --topic     TOPIC       topic for publishing data via REST POST or MQTT
        --rest-timeout  REST_TIMEOUT        how long to wait before stopping REST
        --qos           QOS                 MQTT Quality of Service
            * 0
            * 1
            * 2
        --remote-data       [REMOTE_DATA]       for images, use data from a remote source
        --url               URL                 URL for remote images
        --api-key           API_KEY             API Key associated with remote images
        --authentication    AUTHENTICATION      authentication key for URL
        --exception         [EXCEPTION]         whether to print exceptions
    :params:
        total_rows:int - row counter
        data:list - data to insert into AnyLog
        conns:dict - list of connections with auth information
        last_conn:list - last connection used
        last_blob:str - last image or video used, as to not repeat 2x in a row
    """
    parser = argparse.ArgumentParser(add_help=True, description="Data generator for blobs; used for edgex demo by setting data_type set to edgex")
    parser.add_argument('data_type', type=__data_types, default='edgex',
                        help='type of data to insert into AnyLog. Choices: edgex, video, image')
    parser.add_argument('insert_process', type=__insert_process,  default='print',
                        help='format to store generated data. Choices: print, post, mqtt')
    parser.add_argument('db_name', type=str, default='test', help='logical database name')
    parser.add_argument('--extended-help', type=bool, nargs='?', const=True, action=ExtendedHelpAction, default=False,
                        help="Generates help, but extends to include a sample row per data type")
    parser.add_argument('--conversion-type', type=support.validate_conversion_type, default='base64',
                        help='Format to convert content to be stored in AnyLog. Choices: base64, bytesio, opencv')
    parser.add_argument('--table-name', type=str, default=None,
                       help='Change default table name')
    parser.add_argument('--total-rows', type=support.validate_row_size, default=1000000,
                       help='number of rows to insert. If set to 0, will run continuously')
    parser.add_argument('--batch-size', type=support.validate_row_size, default=10, help='number of rows to insert per iteration')
    parser.add_argument('--sleep', type=float, default=0.5, help='wait time between each row')
    parser.add_argument('--timezone', type=str, choices=['local', 'utc', 'et', 'br', 'jp', 'ws', 'au', 'it'],
                       default='local', help='timezone for generated timestamp(s)')
    parser.add_argument('--enable-timezone-range', type=bool, nargs='?', const=True, default=False,
                       help='set timestamp within a range of +/- 1 month')
    parser.add_argument('--conn', type=support.validate_conn_pattern, default=None,
                       help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('--topic', type=str, default=None, help='topic for publishing data via REST POST or MQTT')
    parser.add_argument('--rest-timeout', type=float, default=30, help='how long to wait before stopping REST')
    parser.add_argument('--qos', type=int, choices=list(range(0, 3)), default=0, help='MQTT Quality of Service')
    parser.add_argument('--remote-data', type=bool, nargs='?', const=True, default=False,
                        help='for images, use data from a remote source')
    parser.add_argument('--url', type=str, default="http://10.31.1.197/v3/predict/e99aefb2-abfc-4ab0-88fb-59e3e8f2b47f",
                        help='URL for remote images')
    parser.add_argument('--api-key', type=str, default='8KK7aDH5fttoV.Dd', help='API Key associated with remote images')
    parser.add_argument('--authentication', type=str, default="b3JpOnRlc3Q", help="authentication key for URL")
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False, help='whether to print exceptions')
    args = parser.parse_args()

    total_rows = 0
    data = []
    if args.batch_size == 0:
        args.batch_size = 10

    conns = None
    if args.conn is not None:
        conns = args.conn.split(',')
    if args.insert_process == "mqtt":
        conns = publish_data.connect_mqtt(conns, exception=args.exception)
        if not conns:
            print("Failed to set connection for MQTT publisher")
            exit(1)
    elif args.insert_process in ["post", "put"]:
        conns = publish_data.setup_put_post_conn(conns=conns)

    last_blob = None
    last_conn = None
    while True:
        if args.data_type == 'edgex':
            if args.table_name is None:
                args.table_name = "people_video"
            payload, last_blob = edgex_data.get_data(db_name=args.db_name, table=args.table_name,
                                                     conversion_type=args.conversion_type, last_blob=last_blob,
                                                     timezone=args.timezone,
                                                     enable_timezone_range=args.enable_timezone_range,
                                                     exception=args.exception)
            if args.insert_process == "print":
                if isinstance(payload["file_content"], bytes):
                    payload["file_content"] = payload["file_content"].decode("utf-8", errors="ignore")
                payload["file_content"] = payload["file_content"][:20] + "..."
        elif args.data_type == 'video':
            if args.table_name is None:
                args.table_name = "videos"
            payload, last_blob = data_generator_videos.video_data(db_name=args.db_name, table=args.table_name,
                                                                  conversion_type=args.conversion_type,
                                                                  last_blob=last_blob, timezone=args.timezone,
                                                                  enable_timezone_range=args.enable_timezone_range,
                                                                  exception=args.exception)

            if args.insert_process == "print":
                if isinstance(payload["file_content"], bytes):
                    payload['readings'][0]['binaryValue'] = payload['readings'][0]['binaryValue'].decode("utf-8", errors="ignore")
                payload['readings'][0]['binaryValue'] = payload['readings'][0]['binaryValue'][:20] + "..."

        elif args.data_type == 'image':
            if args.table_name is None:
                args.table_name = "images"

            payload, last_blob = data_generator_images.image_data(db_name=args.db_name, table=args.table_name,
                                                                  conversion_type=args.conversion_type, url=args.url,
                                                                  api_key=args.api_key, authentication=args.authentication,
                                                                  last_blob=last_blob, remote_data=False,
                                                                  exception=args.exception)

            if args.insert_process == "print":
                if isinstance(payload["file_content"], bytes):
                    payload["file_content"] = payload["file_content"].decode("utf-8", errors="ignore")
                payload["file_content"] = payload["file_content"][:20] + "..."

        data.append(payload)
        if len(data) % args.batch_size == 0:
            last_conn = publish_data.publish_data(payload=data, insert_process=args.insert_process, conns=conns,
                                      topic=args.topic, compress=False, rest_timeout=args.rest_timeout,
                                      qos=args.qos, dir_name=None, last_conn=last_conn,
                                      exception=args.exception)
            data = []

        total_rows += 1
        if total_rows == args.total_rows:
            if len(data) != 0:
                last_conn = publish_data.publish_data(payload=data, insert_process=args.insert_process, conns=conns,
                                                      topic=args.topic, compress=False, rest_timeout=args.rest_timeout,
                                                      qos=args.qos, dir_name=None, last_conn=last_conn,
                                                      exception=args.exception)
            exit(1)

        time.sleep(args.sleep)

if __name__ == '__main__':
    support.validate_packages(is_blobs=True, is_traffic=False)
    main()