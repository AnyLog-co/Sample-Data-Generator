import os
import random

from src.support.file_processing import file_processing
import src.support.timestamp_generator as timestamp_generator
from src.video_processing.video_processing import VideoProcessing

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
DATA_DIR = os.path.join(ROOT_PATH, 'data', 'edgex-demo')
MODEL_FILE = os.path.join(ROOT_PATH, 'data', 'models', 'people.tflite')


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


def __generate_number(file_path:str, expected_value:int)->(int, float):
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
    vp = VideoProcessing(model_file=MODEL_FILE, video=file_path, labels=["0 person"], exception=True)
    if vp.status is True:
        vp.set_interpreter()
    if vp.status is True:
        vp.analyze_data(min_confidence=0.5)
    count, confidence = vp.get_values()

    return count, round(confidence, 3)


def get_data(db_name:str, table:str, conversion_type:str="base64", last_blob:str=None,
             timezone:str="local", enable_timezone_range:bool=False, exception:bool=False)->dict:
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
    if not os.path.isdir(DATA_DIR):
        print(f"Failed to locate directory with images/videos ({DATA_DIR}), cannot continue...")
        exit(1)

    payload = {}
    video = None

    while video == last_blob or video is None:
        video = random.choice(list(DATA))

    full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(DATA_DIR, video)))

    if os.path.isfile(full_file_path):
        count, confidence = __generate_number(file_path=full_file_path, expected_value=DATA[video])
        start_ts, end_ts = timestamp_generator.generate_timestamps_range(timezone=timezone,
                                                                         enable_timezone_range=enable_timezone_range,
                                                                         period=5)

        payload = {
            "dbms": db_name,
            "table": table,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "file_content": file_processing(conversion_type=conversion_type, file_name=full_file_path, exception=exception),
            "count": count,
            "confidence": confidence
        }

    return payload, video
