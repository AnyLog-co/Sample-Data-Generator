"""
1. copy appropriate file(s) into cloud instance (1 time process - manual)
2. convert to select DLB vs DLT
3. begin with `vessel`, then get relevant data file(s) based on timestamp
4. publish data into AnyLog / EdgeLake
"""
import datetime
import json
import posixpath
import time

import source.policies.vessel_mapping
from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient
from source.support import get_files_by_url
from source.policies.mappings import BASE_VESSEL_FILES
from source.policies.mappings import VESSEL_INFO
from source.support import read_json_content
from source.support import timestamp_calculator
from source.northbound.rest_functions import publish_data
from source.policies.mappings import SCHEMA

DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)
VESSEL_COLUMNS = []
for table in VESSEL_INFO:
    if table != "general":
        VESSEL_COLUMNS.extend(VESSEL_INFO.get(table))

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
        side: {group: {file: 0 for file in vessel_files[side][group]} for group in vessel_files[side]} for side in vessel_files
    }


    while is_active:
        for side in vessel_files:
            for id_index, group in enumerate(vessel_files[side]):
                base_row = {
                    "dbms": db_name,
                    "side": side,
                    "boat_name": group.split('_')[0],
                    "timestamp": timestamp_calculator(
                        timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
                        offset=offset_sleep,
                        id_index=id_index
                    )
                }
                if not group.endswith("vessel"):
                    base_row.update({
                        "motor_id": int(group.split('_')[-1]),
                        "ip_index": int(group.split("IP_")[-1].split("_")[0]),
                    })

        #         combine_rows = []
                for file_name in vessel_files.get(side).get(group):
                    print(file_name)
                    row_id = row_counts[side][group][file_name]
                    current_timestamp, file_row = read_json_content(posixpath.join(DATA_DIR, file_name),
                                                                    timestamp=None, row_id=row_id)

                    file_row.update(base_row)
                    publish_data(
                        method=method,
                        conn=conn,
                        topic=TOPIC,
                        payload=file_row,  # ← FIX 3: list not dict
                        db_name=db_name,
                    )
                    insight = {}
                    for table in list(SCHEMA.keys()):
                        if table != "_metadata":
                            for column in file_row:
                                if base_row.get(column) is None and column in SCHEMA[table]:
                                    if table not in insight:
                                        insight[table] = []
                                    insight[table].append(column)

                    print(json.dumps(insight, indent=2))
                    exit(1)


        #             if not file_row:
        #                 for fn in row_counts[side][group]:
        #                     row_counts[side][group][fn] = 0
        #                 break
        #             combine_rows.append(file_row)
        #
        #         rows = [base_row]
        #         for row in combine_rows:
        #             for column in row:
        #                 if column not in rows[0]:
        #                     rows[0][column] = row.get(column)
        #                 else:
        #                     if len(rows) == 1:
        #                         rows.append(base_row)
        #                     rows[-1][column] = row.get(column)



            # print(rows)

        # ── loop control ──────────────────────────────────────────────
        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)


if __name__ == "__main__":
    conn = RestClient(conn="50.116.20.125:32149", auth=(), timeout=30)
    main(method="POST", conn=conn, publish_topics=None, db_name="anotherpeak", iterations=1)