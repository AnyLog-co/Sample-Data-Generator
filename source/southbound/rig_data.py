import posixpath
import time
import zoneinfo
from typing import  Dict
import re

from source.policies.mappings import RIG_INFO
from source.southbound.support import get_files_by_url
from source.southbound.support import url_read_content
from source.southbound.support import calculate_timestamp

from source.northbound.support import publish_data
from source.northbound.rest_calls import RestClient
from source.northbound.mqtt import MqttClient
from source.northbound.opcua import OpcuaServer

DATA_DIR = "http://45.33.11.32/Sample-Data/rig-data/"
RIG_FILES = get_files_by_url(url=DATA_DIR)

TABLE = "rig_data"
TOPIC = "rig-data"

TIMEZONES = {
    1:  zoneinfo.ZoneInfo('America/Chicago'),   # Permian Basin, West Texas    UTC-6
    7:  zoneinfo.ZoneInfo('America/Chicago'),   # Eagle Ford, South Texas      UTC-6
    12: zoneinfo.ZoneInfo('America/Chicago'),   # Bakken, North Dakota         UTC-6
    23: zoneinfo.ZoneInfo('America/Chicago'),   # Gulf of Mexico               UTC-6
    31: zoneinfo.ZoneInfo('America/Denver'),    # Delaware Basin, West Texas   UTC-7
    44: zoneinfo.ZoneInfo('America/Chicago'),   # STACK, Oklahoma              UTC-6
}


def _check_rigs(rig_ids:list[str]|str|None=None)->list:
    """
    Validate Rigs have data (files) and if not specified then set to all rigs
    :args:
        rig_ids:list[str]|str - list of rigs either literal or comma separated string
    :return:
        list of rigs
    """
    if (isinstance(rig_ids, str) and rig_ids.endswith("/#")) or not rig_ids:
        rig_ids = list(RIG_INFO.keys())
    elif isinstance(rig_ids, int) and rig_ids in list(RIG_INFO.keys()):
        rig_ids = [rig_ids]
    elif isinstance(rig_ids, str) or isinstance(rig_ids, list):
        rigs = rig_ids.split(",") if isinstance(rig_ids, str) else rig_ids
        rig_ids = []
        if any(rig.endswith("/#") for rig in rigs):
            rigs_ids = list(RIG_INFO.keys())
        elif not rig_ids:
            for rig in rigs:
                rig = rig.split('/')[-1] if '/' in rig else rig
                if re.match(r"^rig-\d+$", rig):
                    rig = rig.split("-")[-1]
                try:
                    rig = int(rig)
                    file_name = RIG_INFO.get(rig).get("file")
                    if file_name not in RIG_FILES:
                        raise FileNotFoundError(f"Failed to locate {posixpath.join(DATA_DIR, file_name)}")
                    else:
                        rig_ids.append(rig)
                except Exception as error:
                    raise Exception(f"Invalid rig ID {rig} (Error: {error})")

    return rig_ids


def main(method:str, conn:RestClient|MqttClient|OpcuaServer|None, db_name:str, publish_topics:list[str]|str=None,
         iterations:int=10, sleep:float=10, offset_sleep:float=0.5, standalone_values:bool=False, loop=None):
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
        rig_ids:list - based on publish_topics, list of rigs to use
        rig_paths:dict - rigs and their corresponding file paths
        line_count:dict - line counter per rig
        counter:int - iteration counter
        payload:list - payload to publish data
        is_active:bool
        is_null:bool
    """
    rig_ids = _check_rigs(rig_ids=publish_topics)
    rig_paths: Dict[str, str] = {rig_id: posixpath.join(DATA_DIR, RIG_INFO[rig_id]["file"]) for rig_id in rig_ids}
    # line_counts: Dict[str, Optional[int]] = {rig_id: 0 for rig_id in rig_ids}
    line_counts = {
        rig_id: {
            "line_num": 0,
            "timestamp": None
        } for rig_id in rig_ids

    }
    counter = 0
    is_active = True

    while is_active:
        for id_index, (rig_id, file_path) in enumerate(rig_paths.items()):
            row = url_read_content(file_path, line=line_counts[rig_id]["line_num"])

            if row:
                row["timestamp"] = calculate_timestamp(row_id=line_counts[rig_id]["line_num"], off_set=offset_sleep,
                                                       current_timestamp=line_counts[rig_id]["timestamp"],
                                                       timezone=TIMEZONES[rig_id])
                if method in ["MQTT", "POST", "KAFKA"]:
                    row["dbms"] = db_name
                    row["table"] = TABLE

                publish_data(method=method, conn=conn, topic=f"{TOPIC}/rig-{rig_id}", table_name=TABLE,  db_name=db_name,
                             payload=row, standalone_values=standalone_values, loop=loop)

                line_counts[rig_id]["line_num"] += 1
            if row is None:
                line_counts[rig_id]["timestamp"] = None
                line_counts[rig_id]["line_num"] = 0
            elif not line_counts[rig_id]["timestamp"]:
                line_counts[rig_id]["timestamp"] = row["timestamp"]

        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            if all(lc["timestamp"] is None for lc in line_counts.values()):
                for rig_id in line_counts:
                    line_counts[rig_id] = {"line_num": 0, "timestamp": None}
            time.sleep(sleep)


if __name__ == "__main__":
    main(method="PRINT", conn=None, publish_topics=f"{TOPIC}/1", db_name="rig_db",  iterations=5)
