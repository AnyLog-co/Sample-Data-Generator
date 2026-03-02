"""
1. copy appropriate file(s) into cloud instance (1 time process - manual)
2. convert to select DLB vs DLT
3. begin with `vessel`, then get relevant data file(s) based on timestamp
4. publish data into AnyLog / EdgeLake
"""
import datetime
import posixpath
import time

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient
from source.support import get_files_by_url, timestamp_calculator
from source.policies.mappings import BASE_VESSEL_FILES
from source.policies.mappings import VESSEL_INFO
from source.support import get_file_content
from source.northbound.rest_functions import publish_data
from source.support import read_json_content
from source.policies.mappings import SCHEMA
from source.support import find_closest_row

DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)
VESSEL_COLUMNS = []
for table in VESSEL_INFO:
    if table != "general":
        VESSEL_COLUMNS.extend(VESSEL_INFO.get(table))

TOPIC = "vessel-data"
EXPECTED_RESULTS = {table: 0 for table in SCHEMA}
FILE_INDEX = {}
RAW_DATA = {}

def _check_vessels(vessel_ids: list[str] | str = None) -> dict:
    global FILE_INDEX
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

    FILE_INDEX = {
        side: {
            group: {
                file: _preload_file_index(posixpath.join(DATA_DIR, file))
                for file in vessel_files[side][group]
            }
            for group in vessel_files[side]
        }
        for side in vessel_files
    }

    return vessel_files


def _provide_expectations(payload):
    global EXPECTED_RESULTS
    global RAW_DATA
    RAW_DATA = {table: {column: 0 for column in SCHEMA[table]} for table in SCHEMA}

    for row in payload:
        for column in row:
            for table in RAW_DATA:
                if RAW_DATA[table].get(column) is not None:
                    RAW_DATA[table][column] += 1

    for table in EXPECTED_RESULTS:
        EXPECTED_RESULTS[table] = max(list(RAW_DATA[table].values()))


def _preload_file_index(url):
    response = get_file_content(url)
    lines = response.text.splitlines()
    index = []

    for i, line in enumerate(lines):
        if ": {" in line:
            ts_str, json_part = line.split(": ", 1)
            try:
                ts = datetime.datetime.strptime(ts_str.strip(), "%Y-%m-%d %H:%M:%S")
                index.append((ts, i))
            except:
                continue

    return index


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
            base_row = {
                "dbms": db_name,
                "side": side,
                "boat_name": None,
                "timestamp": timestamp_calculator(timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
                                                  offset=offset_sleep,  id_index=list(vessel_files.keys()).index(side))
            }

            target_ts = None
            side_payload = []
            for id_index, group in enumerate(vessel_files[side]):
                if base_row["boat_name"] is None:
                    base_row["boat_name"] = group.split('_')[0]
                if not group.endswith("vessel"):
                    base_row.update({
                        "motor_id": int(group.split('_')[-1]),
                        "ip_index": int(group.split("IP_")[-1].split("_")[0]),
                    })

                for file_name in vessel_files.get(side).get(group):
                    url = posixpath.join(DATA_DIR, file_name)
                    file_index = FILE_INDEX[side][group][file_name]

                    row_id = row_counts[side][group][file_name]
                    if target_ts is not None:
                        row_id = find_closest_row(index=file_index, target_ts=target_ts)
                    target_ts, file_row = read_json_content(url=url, timestamp=None, row_id=row_id)
                    if not file_row:
                        continue

                    file_row.update(base_row)
                    side_payload.append(file_row)

            payload = []
            for row in side_payload:
                if not payload:
                    payload.append(row)
                # If first payload item has None for all keys in row → update it
                elif all(payload[0].get(column) is None for column in row):
                    payload[0].update(row)
                # If ANY existing payload item has all None for row's keys → update that one
                elif any(all(item.get(column) is None for column in row) for item in payload):
                    for item in payload:
                        if all(item.get(column) is None for column in row):
                            item.update(row)
                            break
                # Otherwise append
                else:
                    payload.append(row)

            publish_data(
                method=method,
                conn=conn,
                topic=TOPIC,
                payload=payload,  # ← FIX 3: list not dict
                db_name=db_name,
            )

        # ── loop control ──────────────────────────────────────────────
        payload = []
        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)

#
# if __name__ == "__main__":
#     conn = RestClient(conn="50.116.20.125:32149", auth=(), timeout=30)
#     # conn = RestClient(conn="10.0.0.78:7849", auth=(), timeout=30)
#     main(method="POST", conn=conn, publish_topics=None, db_name="anotherpeak", iterations=10)