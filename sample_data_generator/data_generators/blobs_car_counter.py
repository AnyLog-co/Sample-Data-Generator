import datetime
import os
import random
import sys
import time
import uuid

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split("sample_data_generator")[0]
DATA_GENERATORS = os.path.join(ROOT_PATH, "data_generators")
DATA_DIR = os.path.join(ROOT_PATH, 'data', 'edgex-demo')
MODEL_FILE = os.path.join(ROOT_PATH, 'data', 'models', 'vehicle.tflite')
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, "publishing_protocols")
DATA_DIR = os.path.join(ROOT_PATH, 'data', 'videos')

sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

from sample_data_generator.support.file_processing import file_processing
from sample_data_generator.video_processing.video_processing import VideoProcessing
import sample_data_generator.support.timestamp_generator as timestamp_generator
import sample_data_generator.support.__support__ as support

PROCESS_ID = str(uuid.uuid4())

def __car_counter(file_path:str, exception:bool=False):
    num_cars = []
    speeds = []

    for label in ["car", "truck", "bus"]:
        vp = VideoProcessing(model_file=MODEL_FILE, labels=[f"0 car"], img_process='vehicle', video=file_path,
                             exception=exception)
        vp.set_interpreter()
        vp.process_video(min_confidence=0)
        cars, speed = vp.get_values()
        num_cars.append(cars)
        if 'A.mp4':
            speeds.append(speed * 10)
        else:
            speeds.append(speed * 100)

    avg_speed = sum(speeds)/len(speeds)
    if 'A.mp4' in file_path:
        return int(sum(num_cars)/100), round(avg_speed * 10, 2)
    else:
        return int(int(sum(num_cars) / len(num_cars)) / 100), round(sum(speeds)/len(speeds) * 10, 2)



def __create_data(binary_file:str, file_name:str, db_name:str, start_ts:str, end_ts:str, num_cars:int, speed:float,
                  table_name:str='car_videos', profile_name="anylog-video-generator"):
    data = {
        "apiVersion": "v2",
        "dbName": db_name,
        "id": PROCESS_ID,
        "deviceName": table_name,
        "origin": int(time.time()),
        "profileName": profile_name,
        "readings": [],
        "sourceName": "OnvifSnapshot"
    }

    # file_name = file_name.
    data["readings"].append({
        "timestamp": start_ts,
        "start_ts": start_ts,
        "end_ts": end_ts,
        "binaryValue": binary_file,
        "deviceName": file_name.split(".")[0],
        "id": support.generate_string_hash(file_name=file_name, data=binary_file),
        "mediaType": support.media_type(file_suffix=file_name.rsplit(".", 1)[-1]),
        "origin": int(time.time()),
        "profileName": file_name.split(".")[1],
        "resourceName": "OnvifSnapshot",
        "valueType": "Binary",
        "num_cars": num_cars,
        "speed": speed
    })

    return data


def car_counting(db_name:str, row_count:int, conversion_type:str="base64", sleep:float=0.5, timezone:str="local",
                   last_blob:str=None, enable_timezone_range:bool=False, exception:bool=False):
    payloads = []

    if not os.path.isdir(DATA_DIR):
        print(f"Failed to locate directory with images/videos ({DATA_DIR}), cannot continue...")
        exit(1)

    video = None
    for i in range(row_count):
        while video == last_blob or video is None:
            video = random.choice(list(os.listdir(DATA_DIR)))

        full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(DATA_DIR, video)))
        if os.path.isfile(full_file_path):
            num_cars, avg_speed = __car_counter(file_path=full_file_path, exception=exception)
        print(video, num_cars, avg_speed)
        last_blob  = video

    return payloads, last_blob