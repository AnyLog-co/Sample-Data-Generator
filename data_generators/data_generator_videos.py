import datetime
import os
import sys
import time
import uuid

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, "")
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, "../publishing_protocols")
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import data_generators.file_processing_base64 as file_processing_base64
import data_generators.file_processing_bytesIO as file_processing_bytesIO
import data_generators.file_processing_cv2 as file_processing_cv2
import data_generators.car_insight as car_insight
import publishing_protocols.support as support
import publishing_protocols.publish_data as publish_data


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


def main(dir_name:str="$HOME/Downloads/sample_data/videos", conns:dict={}, protocol:str="post",
         topic:str="video-data", db_name:str="test", table:str="video", sleep:float=5, timezone:str="local",
         timeout:int=30, enable_timezone_range:bool=False, reverse:bool=False, file_base64:bool=True,
         file_byteio:bool=False, file_cv2:bool=False, exception:bool=False):
    """
    Data generator for car traffic videos
    :args:
        dir_name:str - directory containing videos
        conns:str - connection information for either REST or MQTT
        protocol:str - protocol to store data with
            *  print
            * post
            * mqtt
        topic:str - REST / MQTT topic
        db_name:str - logical database name
        table:str - table name
        sleep:float - wait time between each insert
        timezone:str - timezone for generated timestamp(s)
        timeout:int - REST timeout
        enable_timezone_range:bool - set timestamp within a range of +/- 1 month
        reverse:bool - whether to store data in reversed (file) order
        exception:bool - whether to print exceptions
    :params:
        dir_full_path:str - full path of dir_name
        list_dir:str - list of files in dir_name
        full_file_path:str - dir_name + file_name
        car_info:dict - content regarding traffic
        file_content:str - string-bytes of read file
        payload:dict - merged car_info + file_content
    """
    dir_full_path = os.path.expandvars(os.path.expanduser(dir_name))
    list_dir = os.listdir(dir_full_path)
    if reverse is True:
        list_dir = list(reversed(list_dir))

    for file_name in list_dir:
        full_file_path = os.path.join(dir_full_path, file_name)
        car_info = car_insight.car_counter(timezone=timezone, enable_timezone_range=enable_timezone_range)
        if file_base64 is True:
            file_content = file_processing_base64.main(file_name=full_file_path, exception=exception)
        elif file_byteio is True:
            file_content = file_processing_bytesIO.main(file_name=full_file_path, exception=exception)
        elif file_cv2 is True:
            file_content = file_processing_cv2.main(file_name=full_file_path, exception=exception)

        if file_content is not None:
            payload = __create_data(process_id=PROCESS_ID, binary_file=file_content, file_name=file_name,
                                    db_name=db_name, table_name=table, profile_name="anylog-video-generator",
                                    start_ts=car_info["start_ts"], end_ts=car_info["end_ts"], num_cars=car_info["cars"],
                                    speed=car_info["speed"])

            publish_data.publish_data(payload=payload, insert_process=protocol, conns=conns, topic=topic,
                                      rest_timeout=timeout, dir_name=None, compress=False, exception=exception)

        time.sleep(sleep)


