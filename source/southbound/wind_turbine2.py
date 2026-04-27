import copy
import posixpath
import re
import time
import concurrent.futures

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt import MqttClient
from source.northbound.opcua import OpcuaServer
from source.northbound.support import publish_data
from source.southbound.support import get_files_by_url, url_read_content
from source.policies.mappings import WIND_TURBINE_MAPPING


DATA_DIR = "http://45.33.11.32/Sample-Data/wind-turbine2/"

FILE_BREAKDOWN = {
    "farm-1": {
        "turbine-1": "Farm1_WTG1_parameters%2053954%20MV",
        "turbine-2": "Farm1_WTG2_parameters%2053955%20MV",
        "turbine-3": "Farm1_WTG3_parameters%2053956%20MV",
        "turbine-4": "Farm1_WTG4_parameters%2053957%20MV",
    },
    "farm-2": {
        "turbine-1": "Farm2_WTG1_parameters%2053967%20PA",
        "turbine-2": "Farm2_WTG2_parameters%2053968%20PA",
    }
}

TABLE = "wind_turbine2"
TOPIC = "wind-turbine2"


# ─────────────────────────── helpers ────────────────────────────

def _build_topic(farm: str, turbine: str, column: str) -> str:
    """
    Build MQTT-style topic for a column, stripping unit notation.
        "WT1 Active Power [kW]" → "wind-turbine2/farm-1/turbine-1/WT1 Active Power"
    Falls back to stripped column name if not in WIND_TURBINE_MAPPING.
    """
    mapped = WIND_TURBINE_MAPPING.get(column)
    if mapped is None:
        mapped = re.sub(r'\s*\[.*?\]', '', column).strip()
    return f"{TOPIC}/{farm}/{turbine}/{mapped}"


# ─────────────────────────── topic validation ────────────────────────────

def _check_turbines(turbine_ids: list[str] | str) -> None:
    """
    Filter FILE_BREAKDOWN in-place to only the requested farm(s)/turbine(s).

    :args:
        turbine_ids - "#" → all, "farm-1" → all in farm, "farm-1/turbine-2" → specific
    """
    global FILE_BREAKDOWN
    tmp = {}

    if isinstance(turbine_ids, str):
        turbine_ids = turbine_ids.split(",")

    if len(turbine_ids) == 1 and turbine_ids[0] in [None, "#"]:
        return

    for turbine_id in turbine_ids:
        turbine = None
        if '/' in turbine_id:
            farm, turbine = turbine_id.split('/', 1)
        else:
            farm = turbine_id

        if FILE_BREAKDOWN.get(farm) is None:
            raise ValueError(f"Invalid wind farm: {farm}")
        if turbine is not None and turbine != '#' and FILE_BREAKDOWN[farm].get(turbine) is None:
            raise ValueError(f"Invalid turbine: {turbine_id}")

        if turbine in [None, "#"]:
            tmp[farm] = FILE_BREAKDOWN[farm]
        else:
            tmp.setdefault(farm, {})[turbine] = FILE_BREAKDOWN[farm][turbine]

    FILE_BREAKDOWN = copy.deepcopy(tmp)


# ─────────────────────────── worker ────────────────────────────

def _turbine_worker(method: str, conn: RestClient | MqttClient | OpcuaServer | None,
                    farm: str, turbine: str, dir_url: str, db_name: str,
                    iterations: int = 10, sleep: float = 10, offset_sleep: float = 0.5,
                    standalone_values: bool = False, loop=None):
    """
    Worker for a single turbine — runs in its own thread for all methods.

    Directory structure:
        DATA_DIR / farm_dir / turbine_dir / *.json files

    For each row_id:
        - reads that row from every JSON file in the turbine directory
        - builds topic:   wind-turbine2/{farm}/{turbine}/{column}
        - builds payload: {"timestamp": row["Time"], "value": value}
        - adds dbms/table for MQTT, POST, KAFKA
        - publishes via publish_data
        - sleeps offset_sleep between files within the same row group

    When any file returns None the cycle is exhausted; iteration counter
    increments and row_id resets to 0.

    :args:
        method:str         - "POST", "MQTT", "KAFKA", "OPCUA", "PRINT"
        conn:              - active client connection
        farm:str           - e.g. "farm-1"
        turbine:str        - e.g. "turbine-2"
        dir_url:str        - full URL to the turbine's data directory
        db_name:str        - logical database name
        iterations:int     - full cycles to run (0 = run forever)
        sleep:float        - seconds between row groups
        offset_sleep:float - seconds between files within a row group
        standalone_values:bool - publish each key/value as its own topic
        loop               - event loop reference (required for OPCUA)
    """
    for key in FILE_BREAKDOWN:
        if posixpath.join(DATA_DIR, key) in dir_url:
            dir_url = dir_url.replace(posixpath.join(DATA_DIR, key), DATA_DIR)

    try:
        fnames = get_files_by_url(url=dir_url)
    except Exception as error:
        raise Exception(f"Failed to list {dir_url} (Error: {error})")

    if not fnames:
        raise Exception(f"No data files found in {dir_url}")

    file_urls = [posixpath.join(dir_url, fname) for fname in fnames]

    row_id = 0
    iteration_count = 0
    is_active = True

    while is_active:
        cycle_exhausted = False

        for idx, url in enumerate(file_urls):
            row = url_read_content(url=url, line=row_id)

            if row is None:
                cycle_exhausted = True
                break

            timestamp = row.get("Time")

            for column, value in row.items():
                if column == "Time":
                    continue

                topic   = _build_topic(farm, turbine, column)
                payload = {"timestamp": timestamp, "value": value}

                if method in ["MQTT", "POST", "KAFKA"]:
                    payload.update({"dbms": db_name, "table": TABLE})

                try:
                    publish_data(method=method, conn=conn, topic=topic,
                                 table_name=TABLE, db_name=db_name,
                                 payload=payload, standalone_values=standalone_values,
                                 loop=loop)
                except Exception as error:
                    raise Exception(f"Failed to publish {topic} row {row_id} (Error: {error})")

            if idx < len(file_urls) - 1:
                time.sleep(offset_sleep)

        if cycle_exhausted:
            row_id = 0
            iteration_count += 1
            if 0 < iterations <= iteration_count:
                is_active = False
            else:
                time.sleep(sleep)
        else:
            row_id += 1
            time.sleep(sleep)


# ─────────────────────────── main ────────────────────────────

def main(method: str, conn: RestClient | MqttClient | OpcuaServer | None,
         db_name: str = "test", publish_topics: list[str] | str = None,
         iterations: int = 10, sleep: float = 10, offset_sleep: float = 0.5,
         standalone_values: bool = False, loop=None):
    """
    Spin up one thread per turbine and publish its data.

    Directory structure:
        DATA_DIR / {farm_dir} / {turbine_dir} / *.json

    Topic structure:
        wind-turbine2/{farm}/{turbine}/{column}

    :args:
        method:str           - "POST", "MQTT", "KAFKA", "OPCUA", "PRINT"
        conn:                - active client connection
        db_name:str          - logical database name
        publish_topics:      - None / "#" = all, "farm-1" = all in farm,
                               "farm-1/turbine-2" = specific turbine
        iterations:int       - full file cycles per turbine (0 = infinite)
        sleep:float          - seconds between row groups
        offset_sleep:float   - seconds between files within a row group
        standalone_values:bool - publish each key/value as its own topic
        loop                 - event loop reference (required for OPCUA)
    """
    global FILE_BREAKDOWN

    if publish_topics and not (isinstance(publish_topics, str) and publish_topics == "#"):
        _check_turbines(turbine_ids=publish_topics)

    # Build task list: (farm, turbine, full_dir_url)
    # Structure: DATA_DIR / farm / turbine_dir /
    turbine_tasks = [
        (farm, turbine, posixpath.join(DATA_DIR, farm, turbine_dir) + "/")
        for farm, turbines in FILE_BREAKDOWN.items()
        for turbine, turbine_dir in turbines.items()
    ]

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(turbine_tasks)) as executor:
            futures = [
                executor.submit(
                    _turbine_worker,
                    method=method, conn=conn,
                    farm=farm, turbine=turbine, dir_url=dir_url,
                    db_name=db_name,
                    iterations=iterations, sleep=sleep, offset_sleep=offset_sleep,
                    standalone_values=standalone_values, loop=loop,
                )
                for farm, turbine, dir_url in turbine_tasks
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as error:
                    raise Exception(f"Failed to execute turbine thread (Error: {error})")
    except Exception as error:
        raise Exception(f"Failed to run wind_turbine2 (Error: {error})")


if __name__ == "__main__":
    main(method="PRINT", conn=None, db_name="wind_db", publish_topics=["farm-2"], iterations=1)