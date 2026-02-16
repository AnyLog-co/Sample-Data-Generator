import datetime
import json
import time
import posixpath

from source.mappings import RIG_INFO
from source.support import get_files_by_url
from source.support import read_url_content


DATA_DIR = "http://45.33.11.32/Sample-Data/rig-data/"
RIG_FILES = get_files_by_url(url=DATA_DIR)


def __check_rigs(rig_ids:list):
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
            if RIG_INFO[rig_id].get("file") in RIG_FILES:
                file_path = posixpath.join(DATA_DIR, RIG_INFO[rig_id].get("file"))
                payload.append(read_url_content(file_path, line_count))
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


if __name__ == "__main__":
    main(method="POST", conn="test", db_name= "test", rig_ids=None, iterations=10, sleep=10)