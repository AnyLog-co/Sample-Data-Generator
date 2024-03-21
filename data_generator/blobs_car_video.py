import os
import random
import time
import uuid

import data_generator.support as support
from data_generator.video_processing import VideoProcessing

ROOT_PATH = os.path.expandvars(os.path.expanduser(__file__)).split("data_generator")[0]
BLOBS_DIR  = os.path.join(ROOT_PATH, 'blobs', 'car_video')
MODEL_FILE = os.path.join(ROOT_PATH, 'blobs', 'models', 'vehicle.tflite')
PROCESS_ID = str(uuid.uuid4())


def __car_counter(file_path:str, exception:bool=False):
    num_cars = []
    speeds = []

    vp = VideoProcessing(model_file=MODEL_FILE, labels=[f"0 car"], img_process='vehicle', video=file_path,
                         exception=exception)
    vp.set_interpreter()
    vp.process_video(min_confidence=0)
    cars, speed = vp.get_values()
    num_cars.append(cars)
    if 'A.mp4' in file_path:
        speeds.append(speed * 10)
    else:
        speeds.append(speed * 100)

    avg_speed = sum(speeds)/len(speeds)
    if 'A.mp4' in file_path:
        return int(sum(num_cars)/100), round(avg_speed * 10, 2)
    else:
        return int(int(sum(num_cars) / len(num_cars)) / 100), round(sum(speeds)/len(speeds) * 10, 2)


def __create_data(binary_file:str, file_name:str, db_name:str, num_cars:int, speed:float,
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

    # file_name = file_name
    data["readings"].append({
        "timestamp": support.create_timestamp(increase_ts=0),
        "start_ts": support.create_timestamp(increase_ts=0),
        "end_ts": support.create_timestamp(increase_ts=random.choice(list(range(10, 60)))),
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



def car_counting(db_name:str, last_blob:str=None, exception:bool=False):
    if not os.path.isdir(BLOBS_DIR):
        print(f"Failed to locate directory with images/videos ({BLOBS_DIR}), cannot continue...")
        exit(1)

    video = None
    if video is None and last_blob is None:
        while video is None:
            video = random.choice(list(os.listdir(BLOBS_DIR)))
            full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(BLOBS_DIR, video)))
            if not os.path.isfile(full_file_path):
                video = None
    else:
        while video == last_blob or video is None:
            video = random.choice(list(os.listdir(BLOBS_DIR)))
            full_file_path = os.path.expanduser(os.path.expandvars(os.path.join(BLOBS_DIR, video)))
            if not os.path.isfile(full_file_path):
                video = None

    num_cars, avg_speed = __car_counter(file_path=full_file_path, exception=exception)

    binary_file = support.file_processing(file_name=full_file_path, exception=exception)
    payload = __create_data(binary_file=binary_file, file_name=video, db_name=db_name, num_cars=num_cars, speed=avg_speed)

    return payload, video