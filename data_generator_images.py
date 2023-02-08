import json
import os
import random
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(ROOT_PATH, 'data_generators', 'factory_data.json')

DATA_GENERATORS = os.path.join(ROOT_PATH, "data_generators")
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, "publishing_protocols")
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import data_generators.file_processing as file_processing
import publishing_protocols.publish_data as publish_data
import publishing_protocols.support as support


def __get_data(file_name:str, exception:bool)->(list, str):
    """
    From JSON file extract status and detection fro a given file_name
    :args:
        file_name:str - file name to check against in the JSON
        exception:bool - whether to print exceptions to screen
    :params:
        output:dict - raw content from JSON file
        status:str - status value based on file_name
        detection:list - detection value(s) based on file_name
    :return:
        detection, status
    """
    output = None
    status = "Nok"
    detection = []
    try:
        with open(JSON_FILE, 'rb') as f:
            try:
                output = json.load(f)
            except Exception as error:
                if exception is True:
                    print(f"Failed to read content in {JSON_FILE} (Error: {error})")
    except Exception as error:
        if exception is True:
            print(f"Failed to open JSON file {JSON_FILE} (Error: {error})")

    if output is not None and file_name in output and "result" in output[file_name] and "detection" in output[file_name]["result"]:
        detection = output[file_name]["result"]["detection"]
    if output is not None and file_name in output and "status" in output[file_name]:
        status = output[file_name]["status"]

    return detection, status


def __create_data(db_name:str, table:str, file_name:str, file_content:str, detections:list, status:str)->dict:
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
        'dbms': db_name,
        'table': table,
        'file_name': file_name,
        'file_type': support.media_type(file_suffix=file_name.rsplit('.', 1)[-1]),
        'file_content': file_content,
        'detection': detections,
        'status': status
    }

    return payload

def main(dir_name:str="$HOME/Downloads/sample_data/images", conns:str="127.0.0.1:32148", protocol:str="post",
         topic:str="anylog-data-gen", db_name:str="test", table:str="car_data", timeout:int=30,  reverse:bool=False,
         exception:bool=False):
    """
    Data generator for image  - must use images in https://drive.google.com/drive/folders/1EuArx1VepoLj3CXGrCRcxzWZyurgUO3u?usp=share_link
    :args:
        dir_name:str - directory containing videos
        conns:str - connection information for either REST or MQTT
        protocol:str - protocol to store data with
            *  print
            * post
            * mqtt
        topic:str - REST / MQTT topic
        db_name:str - logical database name
        table:str - table name
        timeout:int - REST timeout
        reverse:bool - whether to store data in reversed (file) order
        exception:bool - whether to print exceptions
    :params:
        dir_full_path:str - full path of dir_name
        list_dir:str - list of files in dir_name
        full_file_path:str - dir_name + file_name
        detection:list - list of key/values for a given image
        status:str - whether image is ok or Nok
        file_content:str - string-bytes of read file
        payload:dict - merged car_info + file_content
    """
    dir_full_path = os.path.expandvars(os.path.expanduser(dir_name))
    list_dir = os.listdir(dir_full_path)
    if reverse is True:
        list_dir = list(reversed(list_dir))

    for file_name in list_dir:
        full_file_path = os.path.join(dir_full_path, file_name)
        file_content = file_processing.main(file_name=full_file_path, exception=exception)
        detection, status = __get_data(file_name=file_name, exception=exception)

        if file_content is not None:
            payload = __create_data(db_name=db_name, table=table, file_name=file_name, file_content=file_content,
                                    detections=detection, status=status)

            conn = random.choice(conns.split(','))
            publish_data.publish_data(payload=[payload], insert_process=protocol, conn=conn, topic=topic,
                                      rest_timeout=timeout, dir_name=None, compress=False, exception=exception)

