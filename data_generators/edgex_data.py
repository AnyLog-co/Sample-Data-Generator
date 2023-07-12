
import datetime
import os
import random
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split("data_generators")[0]
DATA_GENERATORS = os.path.join(ROOT_PATH, "data_generators")
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, "publishing_protocols")
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import data_generators.file_processing as file_processing

DATA_DIR = os.path.join(ROOT_PATH, 'data', "edgex-demo")

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


def __generate_number(expected_value:int)->(int, float):
    """
    Generate a number to be used as confidence level
    :args:
        expected_value:int - actual number of people in the video
    :params:
        count:int - calculated guess regarding number of people in video
        confidence:float - how certain the calculation is based on the count
    :return:
        expected_value, confidence
    """
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
        elif confidence == 1:
            confidence = random.random()

    return expected_value, confidence


def get_data(db_name:str, table:str, conversion_type:str="base64", last_blob:str=None, exception:bool=False)->dict:
    """
    Generate payload for EdgeX demo
    :args:
        db_name:str - database to store data in
        table:str - table within the given database
        conversion_type:str - conversion type
        last_blob:str - last blob used
        exception:bool - whether to print exceptions
    :global:
        DATA:dict - video + number of people in the video
        DATA_DIR:str - directory with videos used for demo
    :params:
        payload:dict - generated payload
        video:str - randomly selected video from DATA
        start_ts / end_ts:str - UTC current timestamp
        full_file_path:str - full file path
    :return:
        payload
    """
    payload = {}
    video = None

    if not os.path.isdir(DATA_DIR):
        print(f"Failed to locate dirctory with images/videos ({DATA_DIR}), cannot continue...")
        exit(1)


    while video == last_blob or video is None:
        video = random.choice(list(DATA))

    full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(DATA_DIR, video)))

    if os.path.isfile(full_file_path):
        count, confidence = __generate_number(expected_value=DATA[video])
        start_ts = datetime.datetime.utcnow()
        end_ts = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)

        payload = {
            "dbms": db_name,
            "table": table,
            "start_ts": start_ts.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "end_ts": end_ts.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "file_content": file_processing.main(conversion_type=conversion_type, file_name=full_file_path, exception=exception),
            "count": count,
            "confidence": confidence
        }

    return payload, video

