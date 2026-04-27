import os
import random

import data_generator.support as support

ROOT_PATH = os.path.expandvars(os.path.expanduser(__file__)).split("data_generator")[0]
BLOBS_DIR  = os.path.join(ROOT_PATH, 'blobs', 'people_video')

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


def get_data(db_name:str, last_blob:str=None, exception:bool=False)->dict:
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
    if not os.path.isdir(BLOBS_DIR):
        print(f"Failed to locate directory with images/videos ({BLOBS_DIR}), cannot continue...")
        exit(1)

    payload = {}
    video = None

    if video is None and last_blob is None:
        while video in [None, '.DS_Store']:
            video = random.choice(list(os.listdir(BLOBS_DIR)))
            full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(BLOBS_DIR, video)))
            if not os.path.isfile(full_file_path):
                video = None
    else:
        while video == last_blob or video in [None, '.DS_Store']:
            video = random.choice(list(os.listdir(BLOBS_DIR)))
            full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(BLOBS_DIR, video)))
            if not os.path.isfile(full_file_path) or os.path.isdir(full_file_path):
                video = None


    if video is not None and os.path.isfile(full_file_path):
        count, confidence = __generate_number(expected_value=DATA[video])

        payload = {
            "dbms": db_name,
            "table": 'people_counter',
            "start_ts": support.create_timestamp(increase_ts=0),
            "end_ts": support.create_timestamp(increase_ts=random.choice(list(range(10, 15)))),
            "file_content": support.file_processing(file_name=full_file_path, exception=exception),
            "count": count,
            "confidence": confidence
        }

    return payload, video

