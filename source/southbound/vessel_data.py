"""
1. copy appropriate file(s) into cloud instance (1 time process - manual)
2. convert to select DLB vs DLT
3. begin with `vessel`, then get relevant data file(s) based on timestamp
4. publish data into AnyLog / EdgeLake
"""
import copy
import datetime
import json
import posixpath
import time

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient
from source.support import get_files_by_url
from source.policies.mappings import BASE_VESSEL_FILES
from source.support import read_json_content
from source.support import timestamp_calculator
from source.northbound.rest_functions import publish_data

DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)

TOPIC = "vessel-data"

def _check_vessels(vessel_ids: list[str] | str = None) -> dict:
    vessel_files = {}
    if vessel_ids and isinstance(vessel_ids, str):
        vessels = [vessel_ids]
    elif vessel_ids and isinstance(vessel_ids, list):
        vessels = vessel_ids
    else:
        vessels = ["DLB", "DLT"]

    for base_side in vessels:
        vessel_files[base_side] = {}
        for group in BASE_VESSEL_FILES.get(base_side, {}):
            for fname in BASE_VESSEL_FILES[base_side][group]:
                if fname in VESSEL_FILES and group not in vessel_files[base_side]:
                    vessel_files[base_side][group] = [fname]
                elif fname in VESSEL_FILES:
                    vessel_files[base_side][group].append(fname)
    return vessel_files


def main(method:str, conn:RestClient|MqttClient|None, db_name:str, publish_topics:list[str]|str=None,
         iterations: int = 10, sleep:float=10, offset_sleep:float=0.5):
    """
    main for publishing vessel (boat) data
    :args:
        method:str - method to publish data
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
    :miising:
        1. if DLT / DLB in parallel - then it's 2 threads
    """


    vessel_files = _check_vessels(publish_topics)

    counter = 0
    is_active = True

    # row counter per group
    row_counts = {
        side: {group: 0 for group in vessel_files[side]}
        for side in vessel_files
    }

    while is_active:

        payload = []

        for side in vessel_files:
            for id_index, group in enumerate(vessel_files[side]):

                row_id = row_counts[side][group]
                group_timestamp = None

                # -----------------------------
                # Build General Metadata
                # -----------------------------
                general_params = {
                    "dbms": db_name,
                    "boat_side": side,
                    "timestamp": timestamp_calculator(
                        timestamp=datetime.datetime.now(datetime.timezone.utc),
                        offset=offset_sleep, id_index=id_index
                    ),
                    "vessel_name": None,
                    "ip_index": "",
                    "motor_id": "",
                    "device": ""
                }

                # Handle vessel file separately
                if "_vessel" in group:
                    general_params["vessel_name"] = group.split("_")[1]
                else:
                    parts = group.split("_")
                    general_params.update({
                        "vessel_name": parts[0],
                        "ip_index": int(group.split("_IP_")[1].split("_ID_")[0]),
                        "motor_id": int(group.rsplit("_", 1)[-1]),
                        "device": group.split(f"{side}_")[1].split("_IP")[0]
                    })

                # Ensure string/bool fields are never None (AnyLog requirement)
                for key in ["vessel_name", "device", "boat_side", "dbms"]:
                    if general_params[key] is None:
                        general_params[key] = ""

                full_row = general_params.copy()

                # -----------------------------
                # Merge JSON files
                # -----------------------------
                for fname in vessel_files[side][group]:
                    url = posixpath.join(DATA_DIR, fname)
                    group_timestamp, row = read_json_content(
                        url=url,
                        row_id=row_id,
                        timestamp=group_timestamp
                    )

                    if not row:
                        row_counts[side][group] = 0
                        break

                    full_row.update(row)

                payload.append(full_row)
                row_counts[side][group] += 1

        # -----------------------------
        # Publish
        # -----------------------------
        if payload:
            # for data in payload:
            publish_data(
                method=method,
                conn=conn,
                topic=TOPIC,
                table_name=None,
                db_name=db_name,
                payload=payload
            )

        # -----------------------------
        # Loop control
        # -----------------------------
        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)


if __name__ == "__main__":
    conn = RestClient(conn="50.116.20.125:32149", auth=(), timeout=30)
    main(method="PRINT", conn=conn, publish_topics=["DLT"], db_name="anotherpeak", iterations=1)