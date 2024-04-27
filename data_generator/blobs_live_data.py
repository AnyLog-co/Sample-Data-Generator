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


def __upload_image(exception:bool=False):
    """
    Publish image to OpenHorizon AI tool
    """
    file_name = random.choice(IMGS)
    file_path = os.path.join(BLOBS, file_name)
    files = {'file': open(file_path, 'rb')}
    try:
        r = requests.post("http://35.223.210.200:3002/upload", files=files)
    except Excception as error:
        if exception is True:
            print(f"Failed to upload data into http://35.223.210.200:3002 (Error: {error})")
    else:
        if 200 <= int(r.status_code) <= 299:
            if r.json()['status'] is not True and exception is True:
                print(f"Failed to upload data into http://35.223.210.200:3002 (Error: Invalid data uploaded)")
        elif exception is True:
            print(f"Failed to upload data into http://35.223.210.200:3002 (Network Error: {r.status_code})")

def __get_bbox_info(exception:bool=False):
    """
    BAsed
    """
    try:
        r = requests.get(url="http://35.223.210.200:3002/static/js/image.json")
    except Except as error:
        if exception is True:
            print(f"Failed to get live data from http://35.223.210.200:3002 (Error: {error})")
    else:
        if 200 <= int(r.status_code) <= 299:
            return r.json()['images']
        else:
            if exception is True:
                print(f"Failed to get live data from http://35.223.210.200:3002 (Network Error: {r.status_code})")

def __get_video(video:str, exception:bool=False):
    try:
        r = requests.get(url=f"http://35.223.210.200:3002/{video}")
    except Exception as error:
        if exception is True:
            print(f"Failed to get live data from http://35.223.210.200:3002 (Error: {error})")
    else:
        if 200 <= int(r.status_code) <= 299:
            name = video.rsplit("/")[-1]
            print(os.path.join(BLOBS, f'{name}'))
            with open(os.path.join(BLOBS, f'{name.replace("png", "html")}'), 'w') as f:
                f.write(r.text)
        else:
            print(r.status_code)


def main(exception:bool=False):
    for i in range(2):
        __upload_image(exception=exception)
        bbox_info = __get_bbox_info(exception=exception)
        print(bbox_info)
        time.sleep(5)


if __name__ == '__main__':
    main(exception=True)
