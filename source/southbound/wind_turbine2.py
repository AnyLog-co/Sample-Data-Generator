import asyncio
import copy
import posixpath
import re
import time
import concurrent.futures

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt import MqttClient
from source.northbound.opcua import OpcuaServer
from source.northbound.rest_functions import publish_data
from source.support import get_files_by_url, read_json_content
from  source.policies.mappings import WIND_TURBINE_MAPPING


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

TOPIC = "wind-turbine2"

# ─────────────────────────── helpers ────────────────────────────

def _unpack_row(result) -> dict | None:
    """
    read_json_content returns (None, dict) for line-based JSON files.
    Unpack safely regardless of whether it returns a tuple or a plain dict.
    """
    if result is None:
        return None
    if isinstance(result, tuple):
        return result[1]   # (timestamp_or_None, row_dict)
    return result


def _build_topic(farm: str, turbine: str, column: str) -> str:
    """
    Strip unit notation (e.g. "[-]", "[kW]") from column name and build
    the full MQTT-style topic: farm/turbine/column
        "WT1 - Status b [-]"  →  "farm-1/turbine-1/WT1 - Status b"
    """
    clean_column = re.sub(r'\s*\[.*?\]', '', column).strip()
    return f"{TOPIC}/{farm}/{turbine}/{WIND_TURBINE_MAPPING.get(column)}"


# ─────────────────────────── topic validation ────────────────────────────

def _check_turbine(turbine_ids: list[str] | str):
    """
    Validate and filter FILE_BREAKDOWN to only the requested farm(s)/turbine(s).
    :args:
        turbine_ids:list[str]|str - topic filter(s)
            "#"              → all
            "farm-1"         → all turbines in farm-1
            "farm-2/turbine-1" → specific turbine
    """
    global FILE_BREAKDOWN
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
                    (turbine is not None and turbine != '#')
                    and FILE_BREAKDOWN.get(farm).get(turbine) is None):
                raise ValueError(f"Invalid wind farm / turbine: {turbine_id}")
            elif turbine in [None, "#"]:
                tmp_files_breakdown[farm] = FILE_BREAKDOWN.get(farm)
            else:
                if farm not in tmp_files_breakdown:
                    tmp_files_breakdown[farm] = {}
                tmp_files_breakdown[farm][turbine] = FILE_BREAKDOWN[farm][turbine]

        FILE_BREAKDOWN = copy.deepcopy(tmp_files_breakdown)


# ─────────────────────────── sync worker (MQTT / REST) ────────────────────────────

def _turbine_data(method: str, conn: RestClient | MqttClient, farm: str, turbine: str,
                  dir_url: str, iterations: int = 10, sleep: float = 10, offset_sleep: float = 0.5):
    """
    Worker for a single turbine (runs in its own thread).

    For each row_id:
        - reads that row from every file in the turbine directory
        - publishes one message per column (topic = farm/turbine/column)
        - sleeps offset_sleep between files within the same row group
    Then sleeps `sleep` before moving to the next row_id.
    When any file returns None the cycle is exhausted; iteration counter increments
    and row_id resets to 0.

    :args:
        method:str         - "POST", "MQTT", "PRINT"
        conn:              - active client connection
        farm:str           - e.g. "farm-1"
        turbine:str        - e.g. "turbine-2"
        dir_url:str        - full URL to the turbine's data directory
        iterations:int     - full cycles to run (0 = run forever)
        sleep:float        - seconds between row groups
        offset_sleep:float - seconds between files within a row group
    """
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
            result = read_json_content(url=url, row_id=row_id)
            row = _unpack_row(result)

            if row is None:
                # This file has no more rows → end of this cycle
                cycle_exhausted = True
                break

            timestamp = row.get("Time")

            for column, value in row.items():
                if column == "Time":
                    continue

                topic = _build_topic(farm, turbine, column)
                # payload = {"timestamp": timestamp, "value": value}

                try:
                    if method == "PRINT":
                        print(f"{topic} → {value}")
                    else:
                        publish_data(method=method, conn=conn, topic=topic,
                                     table_name=None, db_name=None, payload=value)
                except Exception as error:
                    raise Exception(f"Failed to publish {topic} row {row_id} (Error: {error})")

            # offset between files within the same row group (skip after last file)
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


# ─────────────────────────── async worker (OPC-UA) ────────────────────────────

async def _turbine_data_opcua(conn: OpcuaServer, farm: str, turbine: str,
                               dir_url: str, iterations: int = 10,
                               sleep: float = 10, offset_sleep: float = 0.5):
    """
    Async mirror of _turbine_data for OPC-UA. Same row-group logic, awaited sleeps.
    """
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
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, read_json_content, url, row_id)
            row = _unpack_row(result)

            if row is None:
                cycle_exhausted = True
                break

            timestamp = row.get("Time")

            for column, value in row.items():
                if column == "Time":
                    continue

                topic = _build_topic(farm, turbine, column)
                payload = {"timestamp": timestamp, "value": value}

                try:
                    await conn.publish_data(topic=topic, payload=payload)
                except Exception as error:
                    raise Exception(f"Failed to publish {topic} row {row_id} (Error: {error})")

            if idx < len(file_urls) - 1:
                await asyncio.sleep(offset_sleep)

        if cycle_exhausted:
            row_id = 0
            iteration_count += 1
            if 0 < iterations <= iteration_count:
                is_active = False
            else:
                await asyncio.sleep(sleep)
        else:
            row_id += 1
            await asyncio.sleep(sleep)


async def _main_opcua(conn: OpcuaServer, iterations: int = 10,
                      sleep: float = 10, offset_sleep: float = 0.5):
    """
    Start OPC-UA server then run all turbine coroutines concurrently.
    """
    await conn.connect()
    try:
        turbine_tasks = [
            (farm, turbine, posixpath.join(DATA_DIR, fname))
            for farm, turbines in FILE_BREAKDOWN.items()
            for turbine, fname in turbines.items()
        ]
        await asyncio.gather(*[
            _turbine_data_opcua(conn=conn, farm=farm, turbine=turbine, dir_url=dir_url,
                                iterations=iterations, sleep=sleep, offset_sleep=offset_sleep)
            for farm, turbine, dir_url in turbine_tasks
        ])
    except Exception as error:
        raise Exception(f"Failed to run wind turbine via OPC-UA (Error: {error})")
    finally:
        await conn.disconnect()


# ─────────────────────────── main ────────────────────────────

def main(method: str, conn: RestClient | MqttClient | OpcuaServer | None,
         publish_topics: list[str] | str = None,
         iterations: int = 10, sleep: float = 10, offset_sleep: float = 0.5):
    """
    Spin up one thread (or coroutine) per turbine and publish its data.

    Topic logic:
        None / "#"           → all farms and turbines
        "farm-1"             → all turbines in farm-1
        "farm-2/turbine-1"   → one specific turbine

    Within each turbine, row i is published across all ~30 files before
    advancing to row i+1.  Turbines run fully independently of each other.

    :args:
        method:str           - "POST", "MQTT", "OPCUA", "PRINT"
        conn:                - active client connection
        publish_topics:      - topic filter(s); None / "#" means all
        iterations:int       - full file cycles per turbine (0 = infinite)
        sleep:float          - seconds between row groups
        offset_sleep:float   - seconds between files within a row group
    """
    global FILE_BREAKDOWN

    if publish_topics and not (isinstance(publish_topics, str) and publish_topics == "#"):
        _check_turbine(turbine_ids=publish_topics)

    if method.upper() == "OPCUA":
        asyncio.run(_main_opcua(conn=conn, iterations=iterations,
                                sleep=sleep, offset_sleep=offset_sleep))
        return

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
                    method=method, conn=conn,
                    farm=farm, turbine=turbine, dir_url=dir_url,
                    iterations=iterations, sleep=sleep, offset_sleep=offset_sleep,
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
    main(method="PRINT", conn=None, publish_topics=["farm-2"], iterations=1)