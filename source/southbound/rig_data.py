import datetime
import posixpath
import time

from typing import Optional, Dict
from source.policies.mappings import RIG_INFO
from source.support import get_files_by_url
from source.support import read_csv_content
from source.support import timestamp_calculator

from source.northbound.rest_functions import publish_data
from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient

DATA_DIR = "http://45.33.11.32/Sample-Data/rig-data/"
RIG_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "rig_data"
TOPIC = "rig-data"


def _check_rigs(rig_ids:list[str]|str)->list:
    """
    Validate Rigs have data (files) and if not specified then set to all rigs
    :args:
        rig_ids:list[str]|str - list of rigs either literal or comma separated string
    :return:
        list of rigs
    """
    if isinstance(rig_ids, str):
        try:
            rig_ids = [int(rig_id) for rig_id in rig_ids.split(",")]
        except Exception as error:
            raise TypeError(f"Rig ID is of wrong type; should be numeric - Options: {', '.join(map(str,list(RIG_INFO.keys())))} (Error: {error})")


    # check if user input is valid and file(s) exist
    if rig_ids:
        for rig_id in rig_ids:
            if rig_id not in RIG_INFO:
                raise ValueError(f"Invalid rig {rig_id} in rig options")
    else:
        rig_ids = list(RIG_INFO.keys())

    for rig_id in rig_ids:
        if rig_id in RIG_INFO:
            file_name = RIG_INFO.get(rig_id).get("file")
            if file_name not in RIG_FILES:
                raise FileNotFoundError(f"Failed to locate {posixpath.join(DATA_DIR, file_name)}")
        else:
            raise ValueError(f"Invalid rig {rig_id} in rig options")

    return rig_ids


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
        rig_ids:list - based on publish_topics, list of rigs to use
        rig_paths:dict - rigs and their corresponding file paths
        line_count:dict - line counter per rig
        counter:int - iteration counter
        payload:list - payload to publish data
        is_active:bool
        is_null:bool
    """
    rig_ids = _check_rigs(rig_ids=publish_topics)
    rig_paths: Dict[str, str] = {rig_id: posixpath.join(DATA_DIR, RIG_INFO[rig_id]["file"]) for rig_id in rig_ids}
    line_counts: Dict[str, Optional[int]] = {rig_id: 0 for rig_id in rig_ids}

    counter = 0
    is_active = True

    while is_active:
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
        for id_index, (rig_id, file_path) in enumerate(rig_paths.items()):
            print(file_path)
            if line_counts[rig_id] is not None:
                row = read_csv_content(file_path, row_id=line_counts[rig_id])
                if row:
                    row["timestamp"] = timestamp_calculator(timestamp=timestamp, offset=offset_sleep, id_index=id_index)
                    if method in ["MQTT", "POST"]:
                        row["dbms"] = db_name
                        row["table"] = TABLE

                    publish_data(method=method, conn=conn, topic=f"{TOPIC}/rig-{rig_id}", table_name=TABLE, db_name=db_name,
                                     payload=row)
                    line_counts[rig_id] += 1
                else:
                    line_counts[rig_id] = 0


        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            if all(lc is None for lc in line_counts.values()):
                for rig_id in line_counts:
                    line_counts[rig_id] = 0
            time.sleep(sleep)


if __name__ == "__main__":
    main(method="POST", conn=None, publish_topics="a", db_name="rig_db",  iterations=5)
