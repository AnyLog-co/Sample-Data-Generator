import json
import os
import random
import requests
import uuid

from src.data_generators.__support_file__ import file_processing
import src.data_generators.__support_timestamp__ as timestamp_generator
import src.publishing_protocols.support as support

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
JSON_FILE = os.path.join(ROOT_PATH, 'data', 'ntt_factory_data.json')
DATA_DIR = os.path.join(ROOT_PATH, 'data', 'images')


def __get_data_remote(url:str, file_path:str, api_key:str,  basic_authorization:str, exception:bool)->(list, str):
    """
    Get data regarding a file from a remote server
    :note:
        Code was used in the NTT demo with Ubiqube (Herve)
    :sample cURL:
        curl --location --request POST 'http://10.31.1.197/v3/predict/e99aefb2-abfc-4ab0-88fb-59e3e8f2b47f' \
            --header 'Content-Type: multipart/form-data' \
            --header 'predictApiKey: 8KK7aDH5fttoV.Dd' \
            --header 'Authorization: Basic b3JpOnRlc3Q=' \
            --form 'imageFile=@"./deeptector/images/20200306202533614.jpg"' \
            --form 'type="image/jpeg"' \
            --form 'filename="./deeptector/images/20200306202533614.jpg"'
    :args:
        url:str - URL path (with http) to get data from
        file_path:str - file with path to get information for
        api_key:str - Access API key
        basic_authorization:str - base64  authorization password
        exception:bool - whether to print exceptions
    :params:
        headers:dict - REST header information
        file_payload:dict - REST file payload
        output:dict - raw content from REST request
        status:str - status value based on file_name
        detection:list - detection value(s) based on file_name
    :return:
        detection, status
    """
    output = {}
    status = "Nok"
    detection = []

    headers = {
        # 'Content-Type': 'multipart/form-data',
        'predictApiKey': api_key,
        'Authorization': f'Basic {basic_authorization}',
    }

    file_payload = {
        'imageFile': None,
        'type': (None, '"image/jpeg"'),
        'filename': None,
    }

    if os.path.isfile(file_path):
        file_payload["filename"] = file_path
        try:
            file_payload["imageFile"] = open(file_path, 'rb')
        except Exception as error:
            if exception is True:
                print(f"Failed to oen {file_payload} (Error: {error})")
            return detection, status

    if file_payload["imageFile"] is not None:
        try:
            r = requests.get(url=url, headers=headers, files=file_payload)
        except Exception as error:
            if exception is True:
                print(f"Failed to get data from {url} (Error: {error})")
        else:
            if int(r.status_code) != 200 and exception is True:
                print(f"Failed to get data from {url} (Network Error: {r.status_code})")
            elif int(r.status_code) == 20:
                try:
                    output = r.json()
                except:
                    output =r.text

    if isinstance(output, dict) and output != {}:
        if 'result' in output and 'detection' in output['result']:
            detection = output['result']['detection']
        if 'status' in output:
            status = output['status']

    return detection, status


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


def __create_data(db_name:str, table:str, file_name:str, file_content:str, detections:list, status:str,
                  timezone:str="local", enable_timezone_range:bool=False)->dict:
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
    timestamp = timestamp_generator.generate_timestamps_range(timezone=timezone, enable_timezone_range=enable_timezone_range)
    payload = {
        'dbms': db_name,
        'table': table,
        'id': str(uuid.uuid4()),
        'timestamp': timestamp,
        'file_name': file_name,
        'file_type': support.media_type(file_suffix=file_name.rsplit('.', 1)[-1]),
        'file_content': file_content,
        'detection': detections,
        'status': status
    }

    return payload


def image_data(db_name:str, table:str, conversion_type:str='base64', timezone:str="local",
               url:str="http://10.31.1.197/v3/predict/e99aefb2-abfc-4ab0-88fb-59e3e8f2b47f",
               api_key:str="8KK7aDH5fttoV.Dd", authentication:str="b3JpOnRlc3Q=", last_blob:str=None,
               enable_timezone_range:bool=False, remote_data:bool=False, exception:bool=False)->(dict, str):
    """
    Based on either live feed data or ntt_factory_data.json file generate payload for an image
    :args:
        db_name:str - database to store content int
        table:str - table associated with database
        conversion_type:str - conversion type
        last_blob:str - last blob used
        remote_data:bool - whether to use remote data
            url:str - URL path (with http) to get data from
            api_key:str - Access API key
            basic_authorization:str - base64  authorization passw
        exception:bool - whether to print exceptions
    :params:
        image:str - current image to use
        full_path:str - full path to read image
        file_content:str - image in some kind of binary format
        detection:list - detection value(s) based on file_namedetection
        status:str - status value based on file_name
    """
    if not os.path.isdir(DATA_DIR):
        print(f"Failed to locate directory with images/videos ({DATA_DIR}), cannot continue...")
        exit(1)

    image = None
    while image == last_blob or image is None:
        image = random.choice(os.listdir(DATA_DIR))
    full_path = os.path.join(DATA_DIR, image)
    file_content = file_processing(conversion_type=conversion_type, file_name=full_path, exception=exception)

    if remote_data is True:
        detection, status = __get_data_remote(url=url, file_path=full_path, api_key=api_key,
                                              basic_authorization=authentication, exception=exception)
    else:
        detection, status = __get_data(file_name=image, exception=exception)

    payload = __create_data(db_name=db_name, table=table, file_name=image, file_content=file_content,
                            detections=detection, status=status, timezone=timezone, enable_timezone_range=enable_timezone_range)

    return payload, image


