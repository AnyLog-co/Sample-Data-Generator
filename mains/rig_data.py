import csv
import datetime
import json
import os
import time

from source.mappings import RIG_INFO

DATA_DIR = os.path.join(__file__.split("data_generator")[0], "data", "rig-data")
if not os.path.isdir(DATA_DIR):
    raise NotADirectoryError(f"Failed to locate data directory {DATA_DIR}")

def __check_rigs(rig_ids:list):
    # check if user input is valid and file(s) exist
    if rig_ids:
        for rig_id in rig_ids:
            if rig_id not in RIG_INFO:
                raise ValueError(f"Invalid rig {rig_id} in rig options")
    else:
        rig_ids = list(RIG_INFO.keys())

    for rig_id in rig_ids:
        file_path = os.path.join(DATA_DIR, RIG_INFO[rig_id].get("file"))
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Failed to locate {file_path}")

    return rig_ids

def __update_rows(row:dict):
    row.pop("rig_name", None)
    row.pop("location", None)

    for key in row:
        if key not in ["timestamp", "rig_id", "activity", "status"]:
            try:
                row[key] = float(row[key])
            except Exception:
                pass

    row["timestamp"] = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
    return row

def main(method:str, conn, db_name:str="test", rig_ids:list|None=None, iterations:int=10, sleep:float=10):
    line_count = 0
    is_active = True
    counter = 0

    rig_ids = __check_rigs(rig_ids=rig_ids)

    while is_active:
        payload = []
        for rig_id in  rig_ids:
            file_path = os.path.join(DATA_DIR, RIG_INFO[rig_id].get("file"))
            # read file
            try:
                with open(file_path, mode='r', encoding="utf-8-sig") as f:
                    data = list(csv.DictReader(f, delimiter=','))
                    payload.append(data[line_count])
            except Exception as error:
                raise Exception(f"Failed to read content from {full_path} (Error: {error})")

        line_count += 1
        if line_count >= 360:
            line_count = 0

        for row_index in range(len(payload)):
            payload[row_index] = __update_rows(payload[row_index])
            if method.upper() in ["MQTT", "POST"]:
                payload[row_index]["dbms"] = db_name
                payload[row_index]["table"] = "rig_data"

        if method.upper() == "MQTT":
            conn.publish_data(topic="rig-data", payload=payload)
        else:
            headers = {
                **({
                       "type": "json",
                       "dbms": db_name,
                       "table": "rig_data",
                       "mode": "streaming"
                   } if method.upper() == "PUT" else {}),
                **({
                       "command": "data",
                       "topic": "rig-data",
                   } if method.upper() == "POST" else {}),
                "User-Agent": "AnyLog/1.23",
                "Content-Type": "text/plain"
            }
            conn.publish_data(headers=headers, payload=json.dumps(payload), method=method.upper())

        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)
