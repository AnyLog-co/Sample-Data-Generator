"""
1. copy appropriate file(s) into cloud instance (1 time process - manual)
2. convert to select DLB vs DLT
3. begin with `vessel`, then get data relevant data file(s) based on timestamp
4. publish data into AnyLog / EdgeLake
"""
import copy
import datetime
import json
import posixpath

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient
from source.support import get_files_by_url
from source.support import read_json_content
from source.policies.mappings import BASE_VESSEL_FILES
from source.support import read_json_content
from source.support import timestamp_calculator

DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)

TOPIC = "vessel-data"

def _check_vessels(vessel_ids: list[str] | str = None) -> dict:
    global VESSEL_FILES
    copy_files = {}
    if vessel_ids and isinstance(vessel_ids, str):
        vessels = [vessel_ids]
    elif vessel_ids and isinstance(vessel_ids, list):
        vessels = vessel_ids
    else:
        vessels = ["DLB", "DLT"]


    for base_side in vessels:
        if base_side in vessels:
            copy_files[base_side] = {}
        for group in BASE_VESSEL_FILES.get(base_side):
            for fname in BASE_VESSEL_FILES[base_side][group]:
                if fname in VESSEL_FILES and group not in copy_files[base_side]:
                    copy_files[base_side][group] = [fname]
                elif fname in VESSEL_FILES:
                    copy_files[base_side][group].append(fname)
    VESSEL_FILES = copy_files





# method:str, conn:RestClient|MqttClient|None, db_name:str, publish_topics:list[str]|str=None, iterations:int=10,
#          sleep:float=10, offset_sleep:float=0.5
def main(publish_topics: list[str] | str = None):
    _check_vessels(publish_topics)
    timestamp = None

    row_id = 0

    for side in VESSEL_FILES:
        general_params = {"boat_side": side}
        for group in VESSEL_FILES[side]:
            general_params.update ({
                "boat_name": group.split('_', 1)[0],
                "ip_index": int(group.split(f"_IP_", 1)[-1].split(f"_ID_", 1)[0]),
                "motor_id": int(group.rsplit('_', 1)[-1])
            })
            general_params["device"] = group.split(f"{general_params.get('boat_side')}_")[-1].split("_IP")[0]
            general_params["timestamp"] = timestamp_calculator(timestamp=datetime.datetime.now(), offset=0, id_index=0)
            full_row = general_params
            print(json.dumps(full_row, indent=2))
            exit(1)
            for fname in VESSEL_FILES[side][group]:
                print(fname)
                url = posixpath.join(DATA_DIR, fname)
                if timestamp is not None:
                    timestamp, row = read_json_content(url=url, row_id=None, timestamp=timestamp)
                else:
                    timestamp, row = read_json_content(url=url, row_id=row_id, timestamp=timestamp)
                # print(row)
                full_row.update(row)
            print(json.dumps(full_row, indent=2))
            exit(1)



if __name__ == "__main__":
    main(publish_topics=["DLT"])