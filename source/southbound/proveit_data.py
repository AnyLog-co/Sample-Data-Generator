import asyncio
import posixpath
import concurrent.futures

from source.northbound.rest_calls import RestClient
from source.northbound.mqtt_calls import MqttClient
from source.northbound.opcua import OpcuaServer
from source.southbound.proveit_support import proveit_data
from source.southbound.proveit_support import proveit_opcua
from source.support import get_files_by_url


DATA_DIR = "http://45.33.11.32/Sample-Data/proveit-data/"
PROVEIT_FILES = get_files_by_url(url=DATA_DIR)

def _check_files_topics(topics:list[str]):
    global PROVEIT_FILES

    for letter in ['A', 'B', 'C']:
        # Check if any topic contains this Enterprise letter
        if not any(f"Enterprise {letter}" in t for t in topics):
            for fname in PROVEIT_FILES:
                if fname.startswith(f"Enterprise_{letter}"):
                    try:
                        PROVEIT_FILES.remove(file_name)
                    except ValueError:
                        # file was not in the list, skip
                        pass



# async def _main_opcua(conn:RestClient|MqttClient|OpcuaServer|None, publish_topics:list[str]|str=None,
#                       iterations:int=10, sleep:float=10, offset_sleep:float=0.5):
#
#     try:
#         await conn.connect()  # connect OPC-UA
#         fname = random.choice
#         await asyncio.gather(
#             *[proveit_opcua(conn=conn, url=posixpath.join(DATA_DIR, fname),
#                             publish_topics=publish_topics, iterations=iterations, sleep=sleep,
#                             offset_sleep=offset_sleep) for fname in PROVEIT_FILES]
#         )
#     except Exception as error:
#         raise Exception(f"Failed to run Proveit via OPC-UA (Error: {error})")
#     finally:
#         await conn.disconnect()


def main(method:str, conn:RestClient|MqttClient|OpcuaServer|None, publish_topics:list[str]|str=None,
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
    global PROVEIT_FILES
    if publish_topics:
        _check_files_topics(topics=publish_topics)


    if method.upper() != "OPCUA":
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(PROVEIT_FILES)) as exec:
                futures = [
                    exec.submit(proveit_data, method=method, conn=conn, url=posixpath.join(DATA_DIR, fname),
                                publish_topics=publish_topics, iterations=iterations, sleep=sleep,
                                offset_sleep=offset_sleep) for fname in PROVEIT_FILES
                ]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as error:
                        raise Exception(f"Failed to execute thread (Error: {error})")
        except Exception as error:
            raise Exception(f"Failed to execute threading from Proveit (Error: {error})")
    else:
        asyncio.run(proveit_opcua(conn=conn, publish_topics=publish_topics, iterations=iterations, sleep=sleep,
                                  offset_sleep=offset_sleep))

#
# if __name__ == "__main__":
#     conn = OpcuaServer(host="0.0.0.0", port=4841)
#     main(method="OPCUA", conn=conn, iterations=0)
