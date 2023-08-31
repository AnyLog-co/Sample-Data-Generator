import datetime
import os
import random
import sys
import time
import uuid

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split("data_generators")[0]
DATA_GENERATORS = os.path.join(ROOT_PATH, "data_generators")
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, "publishing_protocols")
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import source.data_generators.file_processing as file_processing
import source.data_generators.timestamp_generator as timestamp_generator
import source.publishing_protocols.support as support

DATA_DIR = os.path.join(ROOT_PATH, 'data', 'videos')


PROCESS_ID = str(uuid.uuid4())


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



def __car_counter(timezone:str, enable_timezone_range:bool=False)->dict:
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
    hours = datetime.datetime.strptime(start_ts, '%Y-%m-%dT%H:%M:%S.%fZ').hour

    if 5 <= hours < 7:
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
        cars = int(random.choice(range(10, 30)))
    elif 7 <= hours < 10:
        speed = round(random.choice(range(45, 65)) - random.random(), 2)
        cars = int(random.choice(range(40, 60)))
    elif 10 <= hours < 16:
        cars = int(random.choice(range(5, 20)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
    elif 16 <= hours < 20:
        speed = round(random.choice(range(45, 65)) - random.random(), 2)
        cars = int(random.choice(range(40, 60)))
    elif 20 <= hours < 23:
        cars = int(random.choice(range(5, 20)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
    else:  # 23:00 to 5:00
        cars = int(random.choice(range(0, 15)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
    if cars == 0:
        speed = 0

    return {
        'start_ts': timestamp_generator.__timestamp_string(timestamp=start_ts),
        'end_ts': timestamp_generator.__timestamp_string(timestamp=end_ts),
        'cars': cars,
        'speed': speed
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
    file_content = file_processing.main(conversion_type=conversion_type, file_name=full_path, exception=exception)
    car_info = __car_counter(timezone=timezone, enable_timezone_range=enable_timezone_range)

    payload = __create_data(process_id=PROCESS_ID, binary_file=file_content, file_name=video,
                            db_name=db_name, table_name=table, profile_name="anylog-video-generator",
                            start_ts=car_info["start_ts"], end_ts=car_info["end_ts"], num_cars=car_info["cars"],
                            speed=car_info["speed"])

    return payload, video

