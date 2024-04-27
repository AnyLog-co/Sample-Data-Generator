import ast
import json
import os
import time
import random
import requests

ROOT_DIR = os.path.dirname(os.path.expanduser(os.path.expandvars(__file__))).split("data_generator")[0]
BLOBS = os.path.join(ROOT_DIR, 'blobs', 'ibm_imgs')
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


def __upload_image(url:str='35.223.210.200:3002', exception:bool=False):
    """
    Publish image to OpenHorizon AI tool
    """
    file_name = random.choice(IMGS)
    file_path = os.path.join(BLOBS, file_name)
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
                return file_name
        elif exception is True:
            print(f"Failed to upload data into http://{url} (Network Error: {r.status_code})")

def __get_bbox_info(url:str='35.223.210.200:3002', exception:bool=False):
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

def main(url:str='35.223.210.200:3002', exception:bool=False):
    file_name = __upload_image(url=url, exception=exception)
    bbox_info = __get_bbox_info(url=url, exception=exception)
    return file_name, bbox_info
