
import datetime
import os
import random
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, "")
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, "../publishing_protocols")
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import data_generators.file_processing as file_processing


DATA = {
    "edgex2.mp4": 1,
    "edgex6.mp4": 5,
    "edgex9.mp4": 4,
    "edgex13.mp4": 5,
    "edgex10.mp4": 4,
    "edgex7.mp4": 5,
    "edgex1.mp4": 0,
    "edgex11.mp4": 5,
    "edgex5.mp4": 3,
    "edgex12.mp4": 5,
    "edgex4.mp4": 3,
    "edgex8.mp4": 5,
    "edgex3.mp4": 2
}


def __generate_number(expected_value)->(int, float):
    if expected_value < 3:
        count = random.choice(range(0, 3))
    if expected_value < 5:
        count = random.choice(range(2, 5))
    else:
        count = random.choice(range(3, 7))

    try:
        confidence = (1 - abs(expected_value - count) / expected_value)
    except ZeroDivisionError:
        confidence = 0.5
    else:
        if confidence < 0:
            confidence = abs(confidence)

    return expected_value, confidence


def get_data(dir_path:str, conversion_type:str="base64", exception:bool=False)->dict:
    data = {}
    video = random.choice(list(DATA))
    count, confidence = __generate_number(expected_value=DATA[video])
    start_ts = datetime.datetime.utcnow()
    end_ts = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
    full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(dir_path, video)))
    if os.path.isfile(full_file_path):
        data = {
            "start_ts": start_ts.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "end_ts": end_ts.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "file_content": file_processing.main(conversion_type=conversion_type, file_name=full_file_path, exception=exception),
            "count": count,
            "confidence": confidence
        }

    return data

