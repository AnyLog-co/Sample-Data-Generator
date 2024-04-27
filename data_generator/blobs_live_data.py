import ast
import json
import os
import time
import random
import requests


import data_generator.support as support
from data_generator.blobs_video_imgs import __create_data

ROOT_DIR = os.path.dirname(os.path.expanduser(os.path.expandvars(__file__))).split("data_generator")[0]
BLOBS_DIR = os.path.join(ROOT_DIR, 'blobs', 'ibm_imgs')
IMGS = [
    "image_1_1714167592685.jpg",
    "image_2_1714167592685.jpg",
    "image_3_1714167592685.jpg",
    "image_1_1714167824508.jpg",
    "image_2_1714167824508.jpg",
    "image_3_1714167824508.jpg",
    "image_1_1714169448707.jpg",
    "image_2_1714169448708.jpg",
    "image_3_1714169448708.jpg"
]


def __upload_image(last_blob:str, url:str='35.223.210.200:3002', exception:bool=False)->str:
    """
    Publish image to OpenHorizon AI tool
    """
    output = None
    binary_file = None
    if last_blob is None:
        file_name = random.choice(IMGS)
    else:
        file_name = None
        while last_blob == file_name or file_name is None:
            file_name = random.choice(IMGS)
    file_path = os.path.join(BLOBS_DIR, file_name)
    files = {'file': open(file_path, 'rb')}
    try:
        r = requests.post(url=f"http://{url}/upload", files=files)
    except Exception as error:
        if exception is True:
            print(f"Failed to upload data into http://{url} (Error: {error})")
    else:
        if 200 <= int(r.status_code) <= 299:
            if r.json()['status'] is not True and exception is True:
                print(f"Failed to upload data into http://{url} (Error: Invalid data uploaded)")
            elif r.json()['status'] is True:
                output = file_name
                binary_file = support.file_processing(file_name=file_path, exception=exception)
        elif exception is True:
            print(f"Failed to upload data into http://{url} (Network Error: {r.status_code})")
    return output, binary_file

def __get_bbox_info(url:str='35.223.210.200:3002', exception:bool=False)->dict:
    """
    Extract bbox information from OpenHorizon AI tool
    """
    request_param = "image.json"
    if int(random.random()*10) >= 8:
        request_param = "video.json"
    try:
        r = requests.get(url=f"http://{url}/static/js/{request_param}")
    except Exception as error:
        if exception is True:
            print(f"Failed to get live data from http://{url} (Error: {error})")
    else:
        if 200 <= int(r.status_code) <= 299:
            return r.json()['images']
        else:
            if exception is True:
                print(f"Failed to get live data from http://{url} (Network Error: {r.status_code})")

# def get_data(file_name:str=None, url:str='35.223.210.200:3002', exception:bool=False):
#     file_name = __upload_image(file_name=file_name, url=url, exception=exception)
#     bbox_info = __get_bbox_info(url=url, exception=exception)
#
#     file_path = os.path.join(BLOBS, file_name)
#     binary_file = support.file_processing(file_name=full_file_path, exception=exception)
#     payload = __create_data(db_name=db_name, file_name=image, file_content=binary_file, detections=detection,
#                             status=status)

def get_data(db_name:str, last_blob:str=None, url:str='35.223.210.200:3002', exception:bool=False)->(dict, str):
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
    """
    image, binary_file = __upload_image(last_blob=last_blob, url=url, exception=exception)
    data = __get_bbox_info(url=url, exception=exception)
    payloads = []
    for box in data:
        status = 'Ok'
        detection = data[box]['bbox']
        if len(detection) == 0:
            status = 'Nok'
        payload = __create_data(db_name=db_name, file_name=image, file_content=binary_file, detections=detection,
                                status=status)
        payloads.append(payload)
    last_blob = image
    return payloads, last_blob

