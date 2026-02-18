import posixpath
import time

from typing import  Dict
from source.support import get_files_by_url
from source.support import read_json_content

from source.northbound.publish_data import publish_data
from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient

DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "vessel_data"
TOPIC = "vessel-data"


def _check_vessels(vessel_ids:list[str]|str)->list:
    """
    Validate turbines have data (files) and if not specified then set to all wind turbines
    :args:
        vessel_ids:list[str]|str - list of wind turbines either literal or comma separated string
    :return:
        list of wind turbines
    """
    is_file = False
    if isinstance(vessel_ids, str):
        vessel_ids = vessel_ids.split(",")
        
    # check if user input is valid and file(s) exist
    if vessel_ids:
        for vessel_id in vessel_ids:
            for file_name in VESSEL_FILES:
                if vessel_id in file_name:
                    is_file = True
                    break
        if not is_file:
            raise ValueError(f"Invalid vessel side(s) in vessel options")
    else:
        vessel_ids = ["DLB", "DLT"]

    return vessel_ids



def main(method:str, conn:RestClient|MqttClient|None, db_name:str, publish_topics:list[str]|str=None, iterations:int=10,
         sleep:float=10, offset_sleep:float=0.5):
    """
    main for publishing rig data
    :args:
        method:str - method to publish data
            - PUT
            - POST
            - MQTT
        conn:RestClient|MqttClient - connection to publish data
        db_name:str - logical database name
        publish_topics:list[str]|str - (sub) list of rigs to publish data from
        iterations:int - number of iterations to run through
        sleep:float - sleep between each iteration
        offset_sleep:float - if multiple rigs, then sleep between each rig
    :params:
        vessel_ids:list - based on publish_topics, list of rigs to use
        rig_paths:dict - rigs and their corresponding file paths
        line_count:dict - line counter per rig
        counter:int - iteration counter
        payload:list - payload to publish data
        is_active:bool
        is_null:bool
    """
    vessel_ids = _check_vessels(vessel_ids=publish_topics)
    vessel_paths:Dict[str, dict] = {}
    for vessel_id in vessel_ids:
        if vessel_id not in vessel_paths:
            vessel_paths[vessel_id] = {}
        for fname in VESSEL_FILES:
            vessel_paths[vessel_id].update({
                "file_path": posixpath.join(DATA_DIR, fname),
                "line_count": 0
            })

    counter = 0
    is_active = True

    while is_active:
        payload = []
        for vessel_id in vessel_paths:
            if vessel_paths[vessel_id].get("line_count") is not None:
                row = read_json_content(vessel_paths[vessel_id].get("file_path"), row_id=vessel_paths[vessel_id].get("line_count"))

                if row:
                    if method in ["MQTT", "POST"]:
                        row["dbms"] = db_name
                        row["table"] = TABLE

                    payload.append(row)
                    vessel_paths[vessel_id]["line_count"] += 1
                    if len(vessel_ids) > 1:
                        time.sleep(offset_sleep)
                else:
                    vessel_paths[vessel_id]["line_count"] = None

        # print(payload)
        publish_data(method=method, conn=conn, topic=TOPIC, table_name=TABLE, db_name=db_name, payload=payload)

        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            if all(vessel_paths.get(vessel_id).get("line_count") is None for vessel_id in vessel_paths):
                for vessel_id in vessel_paths:
                    vessel_paths[vessel_id]["line_count"] = 0
            time.sleep(sleep)


if __name__ == "__main__":
    main(method="POST", conn=None, db_name="rig_db", publish_topics=None, iterations=5)
