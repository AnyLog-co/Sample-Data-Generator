import copy
import posixpath
import time
import concurrent.futures

from typing import Optional, Dict
from source.support import get_files_by_url, read_json_content, timestamp_calculator
from source.northbound.rest_functions import publish_data
from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient
from source.policies.mappings import WIND_TURBINE_TABLES

DATA_DIR = "http://45.33.11.32/Sample-Data/wind-turbine2/"
TURBINE_FILES = []

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


def _check_turbine(turbine_ids: list[str] | str):
    """
    Validate user provides a proper turbine topic(s) for wind-turbine2
    :args:
        turbine_ids:list[str]|str - list of turbine ID(s) used as topics
            - #
            - farm-1/#
            - farm-2/turbine-2/#
    :global:
        FILE_BREAKDOWN:dict[dict:str] - files to use
    :params:
        tmp_file_breakdown:dict[dict:str] - reference of FILE_BREAKDOWN
    """
    global FILE_BREAKDOWN
    global TURBINE_FILES

    tmp_files_breakdown = {}

    if isinstance(turbine_ids, str):
        turbine_ids = turbine_ids.split(",")

    if not (len(turbine_ids) == 1 and turbine_ids[0] == "#"):
        for turbine_id in turbine_ids:
            turbine = None
            if '/' in turbine_id:
                farm, turbine = turbine_id.split('/')
            else:
                farm = turbine_id
            if FILE_BREAKDOWN.get(farm) is None or (
                    (turbine is not None and turbine != '#') and FILE_BREAKDOWN.get(farm).get(turbine) is None):
                raise ValueError(f"Invalid wind farm turbine {turbine_id}")
            elif farm in ["farm-1", "farm-2"] and turbine in [None, "#"]:
                tmp_files_breakdown[farm] = FILE_BREAKDOWN.get(farm)
            else:
                if farm not in tmp_files_breakdown:
                    tmp_files_breakdown[farm] = {}
                tmp_files_breakdown[farm][turbine] = FILE_BREAKDOWN.get(farm).get(turbine)
        FILE_BREAKDOWN = copy.deepcopy(tmp_files_breakdown)

    for farm in FILE_BREAKDOWN:
        for turbine in FILE_BREAKDOWN[farm]:
            TURBINE_FILES.append(get_files_by_url(url=posixpath.join(DATA_DIR, FILE_BREAKDOWN[farm][turbine])))


def _turbine_data(method: str, conn: RestClient | MqttClient, db_name: str, farm: str, turbine: str,
                  dir_url: str, publish_topics: list[str] | str = None, iterations: int = 10,
                  sleep: float = 10, offset_sleep: float = 0.5):
    """
    Worker function for a single turbine. Reads all ~30 files in the turbine directory
    into memory, then publishes row i across all files together before moving to row i+1.

    :args:
        method:str         - publishing method (POST, MQTT, etc.)
        conn:              - active connection client
        db_name:str        - target database / table name
        farm:str           - farm identifier (e.g. "farm-1")
        turbine:str        - turbine identifier (e.g. "turbine-2")
        dir_url:str        - URL to the turbine's data subdirectory
        publish_topics:    - topic filter(s)
        iterations:int     - number of row-groups to publish (0 = all)
        sleep:float        - seconds to wait between row-groups
        offset_sleep:float - seconds to wait between files within a row-group
    """
    topic = f"{farm}/{turbine}"

    # Load all files in this turbine's directory into memory upfront
    try:
        fnames = get_files_by_url(url=dir_url)
    except Exception as error:
        raise Exception(f"Failed to list turbine directory {dir_url} (Error: {error})")

    all_file_data = []
    for fname in fnames:
        url = posixpath.join(dir_url, fname)
        try:
            all_file_data.append(read_json_content(url=url))
        except Exception as error:
            raise Exception(f"Failed to read {url} (Error: {error})")

    if not all_file_data:
        raise Exception(f"No data files found in turbine directory {dir_url}")

    # Determine how many row-groups to publish
    max_rows = min(len(file_data) for file_data in all_file_data)
    row_groups = range(max_rows) if not iterations else range(min(iterations, max_rows))

    for i in row_groups:
        # Publish row i from each file in quick succession (offset_sleep between files)
        for j, file_data in enumerate(all_file_data):
            try:
                row = file_data[i]
                payload = {
                    "timestamp": timestamp_calculator(row),
                    "farm": farm,
                    "turbine": turbine,
                    "data": row,
                }
                print(payload)
                # publish_data(
                #     method=method,
                #     conn=conn,
                #     db_name=db_name,
                #     table=WIND_TURBINE_TABLES.get(farm, db_name),
                #     topic=topic,
                #     data=payload,
                # )
            except Exception as error:
                raise Exception(f"Failed to publish {topic} file[{j}] row {i} (Error: {error})")

            # Small offset between files in the same row-group, except after the last one
            if j < len(all_file_data) - 1:
                time.sleep(offset_sleep)

        # Full sleep between row-groups
        time.sleep(sleep)


def main(method: str, conn: RestClient | MqttClient, db_name: str, publish_topics: list[str] | str = None,
         iterations: int = 10, sleep: float = 10, offset_sleep: float = 0.5):
    """
    Topic logic:
        - "#" || None        → all farms and turbines
        - "farm-1"           → all turbines in farm-1
        - "farm-2/turbine-1" → specific turbine in a specific farm

    Each turbine runs concurrently. Within each turbine, row i is published
    across all ~30 of its files before advancing to row i+1.

    :args:
        method:str         - publishing method (POST, MQTT, etc.)
        conn:              - active connection client
        db_name:str        - target database / table name
        publish_topics:    - topic filter(s); None or "#" means all
        iterations:int     - row-groups to publish per turbine (0 = all)
        sleep:float        - seconds between row-groups
        offset_sleep:float - seconds between files within a row-group
    """
    global FILE_BREAKDOWN
    _check_turbine(turbine_ids=publish_topics)

    # Flatten FILE_BREAKDOWN → list of (farm, turbine, dir_url)
    turbine_tasks = [
        (farm, turbine, posixpath.join(DATA_DIR, fname))
        for farm, turbines in FILE_BREAKDOWN.items()
        for turbine, fname in turbines.items()
    ]

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(turbine_tasks)) as executor:
            futures = [
                executor.submit(
                    _turbine_data,
                    method=method,
                    conn=conn,
                    db_name=db_name,
                    farm=farm,
                    turbine=turbine,
                    dir_url=dir_url,
                    publish_topics=publish_topics,
                    iterations=iterations,
                    sleep=sleep,
                    offset_sleep=offset_sleep,
                )
                for farm, turbine, dir_url in turbine_tasks
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as error:
                    raise Exception(f"Failed to execute thread (Error: {error})")
    except Exception as error:
        raise Exception(f"Failed to execute threading for wind turbine data (Error: {error})")


if __name__ == "__main__":
    # conn = RestClient(conn="10.0.0.78:7849")
    main(method="POST", conn=None, db_name="wind_turbine", publish_topics=["farm-2"])