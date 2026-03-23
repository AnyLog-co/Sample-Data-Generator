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



import asyncio

async def worker(conn, fname, line_count):
    loop = asyncio.get_running_loop()

    row = await loop.run_in_executor(
        None,
        read_json_content,
        fname,
        line_count
    )

    row = row[1]

    await conn.publish_data(
        topic=row.get("topic"),
        payload=row.get("msg")
    )


async def proveit_opcua(conn, proveit_files, concurrency=25):

    await conn.connect()

    sem = asyncio.Semaphore(concurrency)

    async def limited_worker(fname):
        async with sem:
            await worker(conn, fname, 0)

    while True:
        tasks = [
            asyncio.create_task(limited_worker(fname))
            for fname in proveit_files
        ]
        await asyncio.gather(*tasks)


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
        # print(row)
        row = row[1]
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



