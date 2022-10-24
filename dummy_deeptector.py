import argparse
import json
import os
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import file_processing
import support
import publish_data

DIRECTORY_PATH = os.path.expandvars(os.path.expanduser('$HOME/Downloads/sample_data/images'))


def read_json(excepton:bool=False)->dict:
    data = {}
    if os.path.isfile('deeptector.json'):
        try:
            with open('deeptector.json') as f:
                try:
                    data = json.load(f)
                except Exception as error:
                    print(f'Failed to load JSON data (Error: {error})')
        except Exception as error:
            if excepton is True:
                print(f'Failed to read JSON file (Error: {error})')
    return data

def create_data(dbms:str, table:str, file_name:str, file_content:str, detections:list, status:str)->dict:
    """
    :args:
        dbms:str - logical database name
        table:str - table name
        file_name:str - file data is stored in
        file_content:str - content in file
        detections:list - list results values
        status:str - ok / nok
    :sample payload:
    {
        "id": "f85b2ddc-761d-88da-c524-12283fbb0f21",
        "dbms": "ntt",
        "table": "deeptechtor",
        "file_name": "20200306202533614.jpeg",
        "file_type": "image/jpeg",
        "file_content": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD",
        "detection": [
                {"class": "kizu", "bbox": [666, 275, 682, 291], "score": 0.83249},
                {"class": "kizu", "bbox": [669, 262, 684, 277], "score": 0.83249},
                {"class": "kizu", "bbox": [688, 261, 706,276], "score": 0.72732},
                {"class": "kizu", "bbox": [698, 277, 713, 292], "score": 0.72659},
        ],
        "status": "ok"
    }
    """
    payload = {
        'id': support.generate_string_hash(file_name=file_name, data=file_content),
        'dbms': dbms,
        'table': table,
        'file_name': file_name,
        'file_type': support.media_type(file_suffix=file_name.rsplit('.', 1)[-1]),
        'file_content': file_content,
        'detection': detections,
        'status': status
    }

    return payload


def main():
    """
    Main for deeptector code (using either an existing file or cURL)
    :positional arguments:
        dir_name              image directory path
        conn                  {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        protocol              format to save data       [options; post,mqtt]
    :optional arguments:
        -h, --help                      show this help message and exit
        --topic         TOPIC           topic to send data agaisnt
        --dbms          DBMS            Logical database to store data in
        --table         TABLE           Logical database to store data in
        --sleep         SLEEP           wait time between each round of inserts
        --exception     [EXCEPTION]     whether or not to print exceptions to screen
    :params:
        dir_name:str - full path
        image_data:list - list of images in directory
        list_dir:list - list of files in dir
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_name', type=str, default=DIRECTORY_PATH, help='image directory path')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('protocol', type=str, choices=['post', 'mqtt'], default='post', help='format to save data')
    parser.add_argument('--topic', type=str, default='anylog-data-gen', help='topic to send data agaisnt')
    parser.add_argument('--dbms', type=str, default='ntt', help='Logical database to store data in')
    parser.add_argument('--table', type=str, default='deeptechtor', help='Logical database to store data in')
    parser.add_argument('--sleep', type=int, default=30, help='wait time between each round of inserts')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether or not to print exceptions to screen')
    args = parser.parse_args()

    dir_name = os.path.expandvars(os.path.expanduser(args.dir_name))
    image_data = read_json(excepton=args.exception)

    if not os.path.isdir(dir_name):
        print(f'Failed to locate {dir_name}')
        exit(1)
    if len(image_data) == 0:
        print('Missing imagge data')
        exit(1)

    list_dir = os.listdir(dir_name)
    while True:
        for image in image_data:
            if image in list_dir:
                full_path = os.path.join(dir_name, image)

                file_content = file_processing.main(file_name=full_path, exception=args.exception) # read file

                detection = [] # extract results from IMAGES
                if 'detection' in image_data[image]['result']:
                    detection = image_data[image]['result']['detection']

                # create payload
                payload = create_data(dbms=args.dbms, table=args.table, file_name=image, file_content=file_content,
                                      detections=detection, status=image_data[image]['status'])

                # publish payload
                publish_data.publish_data(payload=payload, insert_process='post', conn=args.conn,
                                          topic=args.topic, rest_timeout=30, dir_name=None,
                                              compress=False, exception=args.exception)
            time.sleep(0.5)
        time.sleep(args.sleep)


if __name__ == '__main__':
    main()
