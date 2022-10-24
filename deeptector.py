import argparse
import json
import os
import requests
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

DIRECTORY_PATH = os.path.expandvars(os.path.expanduser('$HOME/deeptector/images'))

HEADERS = {
    # 'Content-Type': 'multipart/form-data',
    'predictApiKey': '8KK7aDH5fttoV.Dd',
    'Authorization': 'Basic b3JpOnRlc3Q=',
}

FILES = {
    'imageFile': None, # open('/home/anylog/deeptector/images/20200306202533614.jpg', 'rb')
    'type': (None, '"image/jpeg"'),
    'filename': None, # (None, '/home/anylog/deeptector/images/20200306202533614.jpg')
}


def __get_data(url:str, headers:dict, files:dict, exception:bool=False)->dict:
    """
    Get data from live deeptector
    :args:
        url:str - URL to access deeptector
        headers:dict - REST headers
        files:dict - REST files
        exception:bool - whether or not to print error messages
    :params:
        output:dict - content to return
    :sample curl:
    curl --location --request POST 'http://10.31.1.197/v3/predict/e99aefb2-abfc-4ab0-88fb-59e3e8f2b47f' \
        --header 'Content-Type: multipart/form-data' \
        --header 'predictApiKey: 8KK7aDH5fttoV.Dd' \
        --header 'Authorization: Basic b3JpOnRlc3Q=' \
        --form 'imageFile=@"./deeptector/images/20200306202533614.jpg"' \
        --form 'type="image/jpeg"' \
        --form 'filename="./deeptector/images/20200306202533614.jpg"'
     :return;
        ouptut
    """
    output = {}
    try:
        r = requests.post(url=url, headers=headers, files=files)
    except Exception as error:
        if exception is True:
            print(f'Failed to get data from Deeptector (Error: {error})')
    else:
        if int(r.status_code) != 200:
            print(f'Failed to get data from Deeptector (Network Error: {r.status_code})')
        else:
            try:
                output = r.json()
            except Exception as error:
                output = r.text
    return output


def __read_json(json_file:str, excepton:bool=False)->dict:
    """
    Read JSON file
    :args:
        json_file:str - JSON file with path
        exception:bool - whether or not to print exceptions
    :params:
        data:dict - content in JSON file
    :return:
        data
    """
    data = {}
    json_file = os.path.expandvars(os.path.expanduser(json_file))
    if os.path.isfile(json_file):
        try:
            with open(json_file) as f:
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
    The following transfers data from Deeptector into AnyLog either via POST or MQTT.
    :positional arguments:
        dir_name              image directory path
        conn                  {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        protocol              format to save data
            * print
            * post (default)
            * mqtt
    :optional arguments:
        -h, --help                          show this help message and exit
        --topic             TOPIC           topic to send data agaisnt
        --dbms              DBMS            Logical database to store data in
        --table             TABLE           Logical database to store data in
        --json-file         JSON_FILE       JSON file with results to be used as a dummy deeptector
        --deeptector-url    DEEPTECTOR_URL  URL for deeptector
        --sleep             SLEEP           sleep between each image
        --batch-sleep       BATCH_SLEEP     wait time between each round of inserts
        --exception         [EXCEPTION]     whether or not to print exceptions to screen
    :global:
        DIRECTORY_PATH:str - (default) directory of images
        HEADERS:dict - REST header information
        FILES:dict - REST files information
    :params:
        json_data:dict - data from JSON file
        data:dict - content for image
        file_content:str - byte-string of image
        payload:dict - content to store in AnyLog
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_name', type=str, default=DIRECTORY_PATH, help='image directory path')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('protocol', type=str, choices=['print', 'post', 'mqtt'], default='post', help='format to save data')
    parser.add_argument('--topic', type=str, default='anylog-data-gen', help='topic to send data agaisnt')
    parser.add_argument('--dbms', type=str, default='ntt', help='Logical database to store data in')
    parser.add_argument('--table', type=str, default='deeptechtor', help='Logical database to store data in')
    parser.add_argument('--json-file', type=str, default=None, help='JSON file with results to be used as a dummy deeptector')
    parser.add_argument('--deeptector-url', type=str, default=None, help='URL for deeptector')
    parser.add_argument('--sleep', type=float, default=10, help='sleep between each image')
    parser.add_argument('--batch-sleep', type=float, default=30, help='wait time between each round of inserts')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether or not to print exceptions to screen')
    args = parser.parse_args()

    json_data = {}
    if args.json_file is None and args.deeptector_url is None:
        print('Missing Deeptector connection information, cannot continue.')
    elif args.json_file is not None:
        json_data = __read_json(json_file=args.json_file, excepton=args.exception)

    full_path = os.path.expandvars(os.path.expanduser(args.dir_name))
    for image in os.listdir(full_path):
        file_path = os.path.join(full_path, image)
        data = {}
        if args.deeptector_url is not None:
            FILES['imageFile'] = open(file_path, 'rb')
            FILES['filename'] = (None, file_path)
            data = __get_data(url=args.deeptector_url, headers=HEADERS, files=FILES, exception=args.exception)
        elif image in json_data:
            try:
                data = json_data[image]
            except Exception as error:
                data = error

        if not isinstance(data, dict) or sorted(list(data)) != ['result', 'status']:
            print(f'Failed to get data for image {image} (Error; {data})')
        elif data == {}:
            print(f'Failed to get data from {image} (Error: empty data set)')
        else:
            file_content = file_processing.main(file_name=file_path, exception=args.exception)  # read file
            detection = []  # extract results from IMAGES
            if 'detection' in data['result']:
                detection = data['result']['detection']
            # create payload
            payload = create_data(dbms=args.dbms, table=args.table, file_name=image, file_content=file_content,
                                  detections=detection, status=data['status'])
            # publish data
            publish_data.publish_data(payload=payload, insert_process=args.protocol, conn=args.conn,
                                      topic=args.topic, rest_timeout=30, dir_name=None,
                                      compress=False, exception=args.exception)
            time.sleep(args.sleep)
        time.sleep(args.sleep)




if __name__ == '__main__':
    main()