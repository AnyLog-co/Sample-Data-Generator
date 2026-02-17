import datetime
import json
import posixpath

from source.mappings import VESSEL_INFO
from source.support import get_files_by_url
from source.support import read_url_content


DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)

def __check_vessels(vessel_sides:list=None):
    is_file = False
    if vessel_sides:
        for vessel in vessel_sides:
            for file_name in VESSEL_FILES:
                if vessel in file_name:
                    is_file = True
                    break
        if not is_file:
            raise ValueError(f"Invalid vessel side(s) in vessel options")
    else:
        vessel_sides = ["DLB", "DLT"]
    return vessel_sides


def main(method:str, conn, db_name:str="test", vessel_sides:list|None=None, iterations:int=10, sleep:float=10):
    line_count = 0
    is_active = True
    counter = 0

    vessel_sides = __check_vessels(vessel_sides=vessel_sides)

    while is_active:
        payload = {key: [] for key in VESSEL_INFO.keys()}
        for vessel_side in vessel_sides:
            for fname in VESSEL_FILES:
                content = None
                if vessel_side in fname:
                    file_path = posixpath.join(DATA_DIR, fname)
                    content = read_url_content(file_path, line_count)
                if content:
                    for key in payload:
                        if fname.endswith(VESSEL_INFO.get(key).get("file_id")):
                            payload[key].append(content)
                    # payload.append()
        for topic in payload:
            for index in range(len(payload[topic])):
                payload[topic][index]["dbms"] = db_name
                payload[topic][index]["table"] = topic
                payload[topic][index]["timestamp"] = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")
            if method.upper() == "MQTT":
                conn.publish_data(topic=topic, payload=payload[topic])
            elif method.upper() == "POST":
                headers = {
                   "command": "data",
                   "topic": topic,
                    "User-Agent": "AnyLog/1.23",
                    "Content-Type": "text/plain"
                }
                conn.publish_data(headers=headers, payload=json.dumps(payload[topic]), method=method.upper())
            else:
                raise ValueError(f"Invalid publishing method {method.upper()} for wind turbine")

        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)

        # print(json.dumps(payload, indent=2))
        # for topic in payload:



if __name__ == "__main__":
    main(method="POST", conn=None, vessel_sides=None)
