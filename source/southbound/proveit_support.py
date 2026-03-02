import asyncio
import copy
import posixpath
import random
import time

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient
from source.northbound.opcua import OpcuaServer
from source.northbound.rest_functions import publish_data
from source.support import read_json_content
from source.support import get_files_by_url


DATA_DIR = "http://45.33.11.32/Sample-Data/proveit-data/"
PROVEIT_FILES = get_files_by_url(url=DATA_DIR)


async def proveit_opcua(conn:OpcuaServer, publish_topics:list[str]|str=None, iterations:int=10, sleep:float=10,
                        offset_sleep:float=0.5):
    await conn.connect()
    used_topics = []
    counter = True
    is_active = True
    line_count = 0

    last_fname = None
    fname = None

    while is_active:
        while last_fname ==  fname:
            fname = random.choice(PROVEIT_FILES)
        url = posixpath.join(DATA_DIR, fname)
        last_fname = copy.deepcopy(fname)
        # row = read_json_content(url=full_path, row_id=line_count)
        loop = asyncio.get_running_loop()
        row = await loop.run_in_executor(None,  read_json_content,url, line_count)
        if row and (row.get("topic") and (not publish_topics or row.get("topic") in publish_topics)):
            if row.get("topic") in used_topics:
                used_topics = []
                await asyncio.sleep(offset_sleep)

            # await conn.publish_data(topic=row.get("topic"), payload=row.get("msg"))
            try:
                await conn.publish_data(topic=row.get("topic"), payload=row.get("msg"))
            except Exception as e:
                raise Exception(f"Failed to publish {row.get('topic')}: {e}")
            # else:
            #     # print(row.get("topic"))
            #     # exit(1)
            used_topics.append(row.get("topic"))
            line_count += 1
        else:
            line_count = 0
            counter += 1
            if 0 < iterations <= counter:
                is_active = False
            else:
                await asyncio.sleep(sleep)


def proveit_data(method:str, conn:RestClient|MqttClient|OpcuaServer|None, url:str, publish_topics:list[str]|str=None,
                 iterations:int=10, sleep:float=10, offset_sleep:float=0.5):
    """
    1. There are 40 files with data we're reading from.
    2. each file will be considered an iteration
    3. offset sleep occurs when we encounter a repeating topic that already happen
    Args:
        method:
        conn:
        publish_topics:
        iterations:
        sleep:
        offset_sleep:

    Returns:

    """
    used_topics = []
    counter = True
    is_active = True
    line_count = 0

    while is_active:
        row = read_json_content(url=url, row_id=line_count)
        if row and (row.get("topic") and ( not publish_topics or row.get("topic") in publish_topics)):
            if row.get("topic") in used_topics:
                used_topics = []
                time.sleep(offset_sleep)

            # publish
            if method == "PRINT":
                print(row)
            elif method == "OPCUA":
                asyncio.run(_proveit_opcua(conn=conn, publish_topics=publish_topics, iterations=iterations,
                                        sleep=sleep, offset_sleep=offset_sleep))
            else: # there will be an issue with POST
                publish_data(method=method, conn=conn, topic=row.get("topic"), table_name=None,
                             db_name=None, payload=row.get("msg"))
            used_topics.append(row.get("topic"))
            line_count += 1

        else:
            line_count = 0
            counter += 1
            if 0 < iterations <= counter:
                is_active = False
            else:
                time.sleep(sleep)



