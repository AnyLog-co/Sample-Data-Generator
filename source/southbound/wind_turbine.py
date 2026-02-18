import datetime
import posixpath
import time

from typing import Optional, Dict
from source.support import get_files_by_url
from source.support import read_turbine_data

from source.northbound.publish_data import publish_data
from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient
from source.policies.mappings import WIND_TURBINE_TABLES

DATA_DIR = "http://45.33.11.32/Sample-Data/wind-turbine/"
TURBINE_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "wind_turbine"
TOPIC = "wind-turbine"


def _check_turbines(turbine_ids:list[int]|str)->list:
    """
    Validate turbines have data (files) and if not specified then set to all wind turbines
    :args:
        turbine_ids:list[str]|str - list of wind turbines either literal or comma separated string
    :return:
        list of wind turbines
    """
    if isinstance(turbine_ids, str):
        try:
            turbine_ids = [int(turbine_id) for turbine_id in turbine_ids.split(",")]
        except Exception as error:
            raise TypeError(f"Turbine ID is of wrong type should be numeric - between 1 and 11 [except 4] (Error: {error})")

    # check if user input is valid and file(s) exist
    if turbine_ids:
        for turbine_id in turbine_ids:
            if turbine_id < 1 or turbine_id == 4 or turbine_id > 11:
                raise ValueError(f"Invalid turbine {turbine_id} in wind turbine options")
    else:
        turbine_ids = list(range(1, 12))
        del turbine_ids[3]

    for turbine_id in turbine_ids:
        if f"wind_turbine_{turbine_id}.json" not in TURBINE_FILES:
            raise FileNotFoundError(f"Failed to locate {posixpath.join(DATA_DIR, f'wind_turbine_{turbine_id}.json')}")

    return turbine_ids

def _turbine_translate(content:dict)->dict:
    updated_content = {}
    for table in WIND_TURBINE_TABLES:
        for key, value in WIND_TURBINE_TABLES[table].items():
            if key == "timestamp":
                updated_content[key] = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")
            elif content.get(value):
                updated_content[key] = content.get(value)
    return updated_content

def main(method:str, conn:RestClient|MqttClient, db_name:str, publish_topics:list[str]|str=None, iterations:int=10,
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
        turbine_ids:list - based on publish_topics, list of rigs to use
        rig_paths:dict - rigs and their corresponding file paths
        line_count:dict - line counter per rig
        counter:int - iteration counter
        payload:list - payload to publish data
        is_active:bool
        is_null:bool
    """
    method = method.upper()
    turbine_ids = _check_turbines(turbine_ids=publish_topics)
    turbine_paths:Dict[str, str] = {turbine_id: posixpath.join(DATA_DIR, f"wind_turbine_{turbine_id}.json") for turbine_id in turbine_ids}
    line_counts:Dict[str, Optional[int]] = {turbine_id: 0 for turbine_id in turbine_ids}

    counter = 0
    is_active = True

    while is_active:
        payload = []
        for turbine_id, file_path in turbine_paths.items():
            if line_counts[turbine_id] is not None:
                row = read_turbine_data(file_path, row_id=line_counts[turbine_id])

                if row:
                    if method in ["MQTT", "POST"]:
                        row["dbms"] = db_name
                        row["table"] = TABLE

                    payload.append(_turbine_translate(content=row))
                    line_counts[turbine_id] += 1
                    if len(turbine_ids) > 1:
                        time.sleep(offset_sleep)
                else:
                    line_counts[turbine_id] = None

        # print(payload)
        publish_data(method=method, conn=conn, topic=TOPIC, table_name=TABLE, db_name=db_name, payload=payload)

        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            if all(lc is None for lc in line_counts.values()):
                for turbine_id in line_counts:
                    line_counts[turbine_id] = 0
            time.sleep(sleep)


if __name__ == "__main__":
    main(method="POST", conn=None, db_name="rig_db", publish_topics=None, iterations=5)
