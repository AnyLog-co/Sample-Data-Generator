import datetime
import json
import time
import posixpath

from source.mappings import WIND_TURBINE_TABLES
from source.support import get_files_by_url
from source.support import read_url_content


DATA_DIR = "http://45.33.11.32/Sample-Data/wind-turbine/"
WIND_TURBINE_FILES = get_files_by_url(url=DATA_DIR)

def __check_turbines(turbine_ids:list):
    # check if user input is valid and file(s) exist
    if turbine_ids:
        for turbine_id in turbine_ids:
            if turbine_id < 1 or turbine_id > 11:
                raise ValueError(f"Invalid turbine {turbine_id} in turbine options")
    else:
        turbine_ids = list(range(1, 12))
        del turbine_ids[3]

    for turbine_id in turbine_ids:
        if f"wind_turbine_{turbine_id}.json" not in WIND_TURBINE_FILES:
            raise FileNotFoundError(f"Failed to locate {posixpath.join(DATA_DIR, f'wind_turbine_{turbine_id}.json')}")

    return turbine_ids

def __update_rows(row:dict):
    updated_row = {}
    for table in WIND_TURBINE_TABLES:
        for key, value in WIND_TURBINE_TABLES[table].items():
            if key == "timestamp":
                updated_row[key] = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
            else:
                updated_row[key] = row.get(value.strip())

    return updated_row

def main(method:str, conn, db_name:str="test", turbine_ids:list|None=None, iterations:int=10, sleep:float=10):
    line_count = 0
    is_active = True
    counter = 0

    turbine_ids = __check_turbines(turbine_ids)
    while is_active:
        payload = []
        for turbine_id in turbine_ids:
            file_path = posixpath.join(DATA_DIR, f"wind_turbine_{turbine_id}.json")
            row = read_url_content(file_path, line_count, encoding='utf-8-sig')
            print(row)
            payload.append(__update_rows(row))

        line_count += 1
        if line_count >= 360:
            line_count = 0

        for row_index in range(len(payload)):
            payload[row_index] = __update_rows(payload[row_index])
            if method.upper() in ["MQTT", "POST"]:
                payload[row_index]["dbms"] = db_name
                payload[row_index]["table"] = "rig_data"

        if method.upper() == "MQTT":
            conn.publish_data(topic="wind-turbine", payload=payload)
        elif method.upper() == "POST":
            headers = {
               "command": "data",
               "topic": "wind-turbine",
                "User-Agent": "AnyLog/1.23",
                "Content-Type": "text/plain"
            }
            conn.publish_data(headers=headers, payload=json.dumps(payload), method=method.upper())
        else:
            raise ValueError(f"Invalid publishing method {method.upper()} for wind turbine")
        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)


if __name__ == "__main__":
    main(method="POST", conn="test", db_name= "test", turbine_ids=None, iterations=10, sleep=10)