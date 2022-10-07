import datetime
import os
import random
import sys


def generate_timestamp(now:datetime.datetime)->(datetime.datetime, datetime.datetime):
    """
    Given current timestamp, generate start/end time(s)
    :args:
        now:datetime.datetime - base timestamp
    :params:
        start:datetime.datetime - "starting" timestamp
        end:datetime.datetime - "ending" timestamp
    :return:
        start, end
    """
    start = now + datetime.timedelta(hours=int(random.random() * 5))
    end = start + datetime.timedelta(seconds=30, microseconds=random.choice(range(0, 999999)))
    return start, end


def car_counter(timestamp:datetime.datetime)->(float, int):
    """
    Generate (avg) cars speed + number of cars
    :args:
        timestamp:datetime.datetime - timestamp to be used for calculations
    :params:
        hours:int - from timestamp extract hour value
        speed:float - "avg" car speed
        cars:int - number of cars on the road
    :return:
        speed, car
    """
    hours = timestamp.hour

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
    else: # 23:00 to 5:00
        cars = int(random.choice(range(0, 15)))
        speed = round(random.choice(range(60, 80)) + random.random(), 2)
        if cars == 0:
            speed = 0

    return speed, cars


def create_data(process_id:str, file_name:str, binary_file:str, device_name:str="anylog-data-generator",
                start_ts:str=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                end_ts:str=(datetime.datetime.utcnow() + datetime.timedelta(seconds=5)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                profile_name="anylog-video-generator", num_cars:int=0, speed:float=0, db_name:str='edgex')->dict:
    """
    Given the user information, create a JSON object
    :args:
        process_id:str - generated UUID process
        files_dict:dict - content to store
        device_name:str - name of device data is coming from
        profile_name:str - name of device profile data is coming from
        db_name:str - logical database name
    :params:
        data:dict - placeholder for JSON object to be stored in AnyLog
        file_name:str - file name without path
    :return:
        data
    :sample json:
    {
        "apiVersion": "v2",
        "id": "6b055b44-6eae-4f5d-b2fc-f9df19bf42cf",
        "deviceName": "anylog-data-generator",
        "origin": 1660163909,
        "profileName": "anylog-video-generator",
        "readings": [{
            "dbms': 'edgex",
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
        "id": process_id,
        "deviceName": device_name,
        "origin": int(time.time()),
        "profileName": profile_name,
        "readings": [],
        "sourceName": "OnvifSnapshot"
    }

    # file_name = file_name.
    data['readings'].append({
        "dbms": db_name,
        "timestamp": start_ts.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "start_ts": start_ts.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "end_ts": end_ts.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "binaryValue": binary_file,
        "deviceName": file_name.split('.')[0],
        "id": __generate_string_hash(file_name=file_name, data=binary_file),
        "mediaType": __media_type(file_suffix=file_name.rsplit('.', 1)[-1]),
        "origin": int(time.time()),
        "profileName": file_name.split('.')[1],
        "resourceName": "OnvifSnapshot",
        "valueType": "Binary",
        "num_cars": num_cars,
        "speed": speed
    })

    return data



