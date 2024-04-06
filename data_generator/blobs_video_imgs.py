import os
import random
import uuid

import data_generator.support as support

ROOT_PATH = os.path.expandvars(os.path.expanduser(__file__)).split("data_generator")[0]
BLOBS_DIR  = os.path.join(ROOT_PATH, 'blobs', 'video_imgs')
JSON_FILE = os.path.join(ROOT_PATH, 'blobs', 'image_data.json')
JSON_CONTENT = []

def __read_data(file_name:str, exception:bool=False):
    try:
        if JSON_CONTENT[file_name]['bbox']:
            detection = JSON_CONTENT[file_name]["bbox"]
    except:
        detection = []
    try:
        if JSON_CONTENT[file_name]['status']:
            status = JSON_CONTENT[file_name]['status']
    except:
        status = 'Nok'

    return detection, status



def __create_data(db_name:str, file_name:str, file_content:str, detections:list, status:str)->dict:
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
    data = {
        'id': str(uuid.uuid4()),
        'dbms': db_name,
        'table': 'video_imgs',
        'timestamp': support.create_timestamp(increase_ts=0),
        'elapseTime': 100 + round(random.random() * random.choice(list(range(300, 700))), 6),
        'file_name': file_name,
        'file_content': file_content,
        'bbox': [],
        'name': 'demo_model',
        'version': 2.0,
        "confidentCutoff": round(random.random(), 2),
        "platform": "linux:x64",
        "cameraDisabled": True,
        "remoteCamerasOn": "false"
    }
    if len(detections) > 0:
        data['bbox'] = detections

    return data


def get_data(db_name:str, last_blob:str=None, exception:bool=False)->(dict, str):
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
    image = None
    global JSON_CONTENT
    detection=[]
    status='Nok'

    if not os.path.isdir(BLOBS_DIR):
        print(f"Failed to locate directory with images/videos ({BLOBS_DIR}), cannot continue...")
        exit(1)

    if image is None and last_blob is None:
        while image in [None, '.DS_Store']:
            image = random.choice(list(os.listdir(BLOBS_DIR)))
            full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(BLOBS_DIR, image)))
            if not os.path.isfile(full_file_path):
                image = None
    else:
        while image == last_blob or image in [None, '.DS_Store']:
            image = random.choice(list(os.listdir(BLOBS_DIR)))
            full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(BLOBS_DIR, image)))
            if not os.path.isfile(full_file_path):
                image = None

    if image is not None and os.path.isfile(full_file_path):
        binary_file = support.file_processing(file_name=full_file_path, exception=exception)
        if os.path.isfile(JSON_FILE):
            JSON_CONTENT = support.read_json_file(file_path=JSON_FILE)
        if JSON_CONTENT != []:
            detection, status = __read_data(file_name=image, exception=exception)

        payload = __create_data(db_name=db_name, file_name=image, file_content=binary_file, detections=detection,
                                status=status)

    last_blob = image
    return payload, last_blob

