import copy
import posixpath
import zoneinfo
import time

from source.policies.mappings import BASE_VESSEL_FILES
from source.policies.mappings import VESSEL_INFO
from source.policies.mappings import VESSEL_SCHEMAS

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt import MqttClient
from source.northbound.opcua import OpcuaServer

# from source.southbound.support import get_files_by_url
from source.southbound.support import get_files_by_url
from source.southbound.support import url_read_content
from source.southbound.support import calculate_timestamp
from source.northbound.support import publish_data


DATA_DIR = "http://45.33.11.32/Sample-Data/vessel-data/"
VESSEL_FILES = get_files_by_url(url=DATA_DIR)
VESSEL_COLUMNS = []
for table in VESSEL_INFO:
    if table != "general":
        VESSEL_COLUMNS.extend(VESSEL_INFO.get(table))

TOPIC = "vessel-data"
EXPECTED_RESULTS = {table: 0 for table in VESSEL_SCHEMAS}
FILE_INDEX = {}
RAW_DATA = {}

def _check_vessels(vessel_ids:list[str]|str=None)->dict:
    global FILE_INDEX
    tmp = {}
    vessel_files = {"DLB": {}, "DLT": {}}


    if vessel_ids and (isinstance(vessel_ids, str) or isinstance(vessel_ids, list)):
        vessel_ids = vessel_ids.split(",") if isinstance(vessel_ids, str) else vessel_ids
        if not any(vessel.endswith("/#") for vessel in vessel_ids):
            vessel_files = {}
            for vessel in vessel_ids:
                if "DLB" in vessel:
                    vessel_files["DLB"] = {}
                elif "DLT" in vessel:
                    vessel_files["DLT"] = {}

    for base_side in vessel_files:
        for group in BASE_VESSEL_FILES.get(base_side):
            if vessel_files.get(base_side).get(group) is None:
                vessel_files[base_side][group]  = []
            if BASE_VESSEL_FILES.get(base_side).get(group):
                for fname in BASE_VESSEL_FILES.get(base_side).get(group):
                    vessel_files[base_side][group].append(fname)

    for side in vessel_files:
        tmp[side] = {
            "line_num": {},
            "timestamp": {}
        }
        for group in vessel_files.get(side):
            for fname in vessel_files.get(side).get(group):
                tmp[side]["line_num"][fname] = 0
                tmp[side]["timestamp"][fname] = None

    vessel_files = copy.deepcopy(tmp)
    return vessel_files



def main(method:str, conn:RestClient|MqttClient|OpcuaServer|None, db_name:str, publish_topics:list[str]|str=None,
         iterations:int = 10, sleep:float=10, offset_sleep:float=0.5, standalone_values:bool=False, loop=None):
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
    :mising:
        1. if DLT / DLB in parallel - then it's 2 threads
    """
    vessel_files = _check_vessels(publish_topics)

    counter = 0
    is_active = True

    while is_active:
        for side in vessel_files:
            base_row = {
                "dbms": db_name,
                "side": side,
                "boat_name": None,
                "motor_id": None,
                "ip_index": None
            }

            payload = []
            for filename in vessel_files.get(side).get("line_num"):
                file_path = posixpath.join(DATA_DIR, filename)
                filename_to_base = filename.split(".json")[0]
                if filename_to_base.endswith("DEVICE"):
                    filename_to_base = filename_to_base.rsplit("_DEVICE")[0]
                base_row["boat_name"] = filename_to_base.split("_")[1] if not base_row.get("boat_name") else base_row.get("boat_name")

                if not filename_to_base.endswith("vessel"):
                    try:
                        base_row.update({
                            "motor_id": int(filename_to_base.split('_')[-1]),
                            "ip_index": int(filename_to_base.split("IP_")[-1].split("_")[0]),
                        })
                    except: 
                        print(filename_to_base)
                        exit(1)

                row = url_read_content(file_path, line=vessel_files.get(side).get("line_num").get(filename))

                if row:
                    row.update(base_row)
                    row["timestamp"] = calculate_timestamp(row_id=vessel_files[side]["line_num"][filename], off_set=offset_sleep,
                                                           current_timestamp=vessel_files.get(side).get("timestamp").get(filename),
                                                           timezone=zoneinfo.ZoneInfo("Europe/Zurich"))
                    if not vessel_files[side]["timestamp"][filename]:
                        vessel_files[side]["timestamp"][filename] = row["timestamp"]
                    row["side"] = side
                    if method in ["MQTT", "POST", "KAFKA"]:
                        row["dbms"] = db_name
                    payload.append(row)
                    vessel_files[side]["line_num"][filename] += 1
                else:
                    vessel_files[side]["timestamp"][filename] = None
                    vessel_files[side]["line_num"][filename] = 0

            publish_data(method=method, conn=conn, topic=f"{TOPIC}/{side}",
                         table_name="boat_insight" if method == "PUT" else None,
                         db_name=db_name, payload=payload, standalone_values=standalone_values, loop=loop)

        if iterations > 0 and 0 < counter < iterations:
            is_active = False
        else:
            counter +=  1
            time.sleep(sleep)

if __name__ == "__main__":
    # conn = RestClient(conn="50.116.20.125:32149", auth=(), timeout=30)
    # conn = RestClient(conn="10.0.0.78:7849", auth=(), timeout=30)
    conn = MqttClient(host="127.0.0.1", port=32150, timeout=90)
    main(method="MQTT", conn=conn, publish_topics="DLT", db_name="mydb", iterations=10)
