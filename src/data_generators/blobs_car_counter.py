import datetime
import os
import random
import time
import uuid

from src.support.file_processing import file_processing
import src.support.timestamp_generator as timestamp_generator
import src.support.__support__ as support

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
DATA_DIR = os.path.join(ROOT_PATH, 'data', 'videos')
MODEL_FILE = os.path.join(ROOT_PATH, 'data', 'models', 'models', 'vehicle.tflite')
PROCESS_ID = str(uuid.uuid4())

from src.video_processing.video_processing import VideoProcessing


def __create_data(process_id:str, file_name:str, binary_file:str, db_name:str="test", table_name:str="edgx_images",
                  start_ts:str=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                  end_ts:str=(datetime.datetime.utcnow() + datetime.timedelta(seconds=5)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                  profile_name="anylog-video-generator", num_cars:int=0, speed:float=0)->dict:
    """
    Given the user information, create a JSON object
    :args:
        process_id:str - generated UUID process
        files_dict:dict - content to store
        table_name:str - table name
        device_name:str - name of device data is coming from
        profile_name:str - name of device profile data is coming from
    :params:
        data:dict - placeholder for JSON object to be stored in AnyLog
        file_name:str - file name without path
    :return:
        data
    :sample json:
    {
        "apiVersion": "v2",
        "dbName": {db_name}
        "id": "6b055b44-6eae-4f5d-b2fc-f9df19bf42cf",
        "deviceName": {table_name},
        "origin": 1660163909,
        "profileName": "anylog-video-generator",
        "readings": [{
            "start_ts": "2022-01-01 00:00:00",
            "end_ts": "2022-01-01 00:00:05",
            "binaryValue": "AAAAHGZ0eXBtcDQyAAAAAWlzb21tcDQxbXA0MgADWChtb292AAAAbG12aGQAAAAA3xnEUt8ZxFMAAHUwAANvyQABAA",
            "mediaType": "video/mp4",
            "origin": 1660163909,
            "profileName": "traffic_data",
            "resourceName": "OnvifSnapshot",
            "valueType": "Binary",
            "num_cars": 5,
            "speed": 65.3
        }],
        "sourceName": "OnvifSnapshot"
    }
    """
    data = {
        "apiVersion": "v2",
        "dbName": db_name,
        "id": process_id,
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


def __car_counter(file_path:str, timezone:str, enable_timezone_range:bool=False)->dict:
    """
    Generate car insight information
    :params:
        start_ts:datetime.datetime - UTC current timestamp
        end_ts:datetime.datetime - current timestamp + 5 to 90 seconds into the future
        hours:int - hour based on start_ts
        cars:int - number of cars passed at a given hour
        speed:float - avg car speed
    :return:
        dictionary object of
            - start_ts
            - end_ts
            - cars
            - speed
    """
    start_ts, end_ts = timestamp_generator.generate_timestamps_range(timezone=timezone, enable_timezone_range=enable_timezone_range)

    num_cars = {}
    avg_speed = {}
    total_time = 0
    for label in ["car", "truck", "bus"]:
        start_time = time.time()
        vp = VideoProcessing(model_file=MODEL_FILE, labels=[f"0 {label}"], img_process='vehicle', video=file_path, exception=True)
        if vp.status is True:
            vp.set_interpreter()
        if vp.status is True:
            total_time += time.time() - start_time
            cars, speed = vp.get_values()
            num_cars[label] = cars
            avg_speed[label] = speed
    if 'A.mp4':
        total_cars = int(sum(num_cars.values()))
    else:
        total_cars = int(sum(num_cars.values()) / len(num_cars))
    avg_speed = sum(avg_speed.values())/len(avg_speed)

    return {
        'start_ts': timestamp_generator.__timestamp_string(timestamp=start_ts),
        'end_ts': timestamp_generator.__timestamp_string(timestamp=end_ts),
        'cars': total_cars,
        'speed': round(avg_speed, 3)
    }

def video_data(db_name:str, table:str, conversion_type:str='base64', last_blob:str=None,
               timezone:str="local", enable_timezone_range:bool=False, exception:bool=False)->(dict, str):

    if not os.path.isdir(DATA_DIR):
        print(f"Failed to locate directory with images/videos ({DATA_DIR}), cannot continue...")
        exit(1)

    video = None
    while video == last_blob or video is None:
        video = random.choice(os.listdir(DATA_DIR))
    full_path = os.path.join(DATA_DIR, video)
    file_content = file_processing(conversion_type=conversion_type, file_name=full_path, exception=exception)
    car_info = __car_counter(file_path=full_path, timezone=timezone, enable_timezone_range=enable_timezone_range)

    payload = __create_data(process_id=PROCESS_ID, binary_file=file_content, file_name=video,
                            db_name=db_name, table_name=table, profile_name="anylog-video-generator",
                            start_ts=car_info["start_ts"], end_ts=car_info["end_ts"], num_cars=car_info["cars"],
                            speed=car_info["speed"])

    return payload, video

