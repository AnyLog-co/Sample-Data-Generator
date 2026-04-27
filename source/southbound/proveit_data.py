import threading
import posixpath
import time
from typing import Dict, List

from source.southbound.support import get_files_by_url, url_read_content
from source.northbound.support import publish_data
from source.northbound.rest_calls import RestClient
from source.northbound.mqtt import MqttClient
from source.northbound.opcua import OpcuaServer

DATA_DIR = "http://45.33.11.32/Sample-Data/proveit-data2/"
ALL_FILES = get_files_by_url(url=DATA_DIR)

TOPIC_ROOT = "proveit"


def _extract_files(topics: str | List[str] | None = None) -> Dict[str, List[str]]:
    """
    Return mapping of topic -> list of files
    """
    if isinstance(topics, str):
        topics = topics.split(",")

    topics = topics or ["Enterprise_A", "Enterprise_B", "Enterprise_C"]

    topic_files: Dict[str, List[str]] = {}

    for fname in ALL_FILES:
        for topic in topics:
            if fname.startswith(topic) and topic == "Enterprise_C":
                full_topic = f"Enterprise_C/{fname.split('.')[1]}"
                if full_topic not in topic_files:
                    topic_files[full_topic] = []
                topic_files[full_topic].append(fname)
            elif fname.startswith(topic):
                if topic not in topic_files:
                    topic_files[topic] = []
                topic_files[topic].append(fname)

    if not any(topic_files.values()):
        raise Exception("No matching files found")

    return topic_files


def _topic_worker(
    topic_name: str,
    files: List[str],
    method: str,
    conn: RestClient | MqttClient | OpcuaServer | None,
    db_name: str,
    iterations: int,
    sleep: float,
    offset_sleep: float,
    standalone_values: bool,
    loop,
):
    """
    One worker per topic (runs in its own thread)
    """

    file_paths = [posixpath.join(DATA_DIR, f) for f in files]

    # track line per file
    line_counts = [0 for _ in file_paths]

    counter = 0
    is_active = True

    while is_active:
        for idx, file_path in enumerate(file_paths):
            row = url_read_content(file_path, line=line_counts[idx])

            if row:
                msg = row.get("msg")
                sub_topic = row.get("topic") or topic_name

                if msg:
                    publish_data(
                        method=method,
                        conn=conn,
                        topic=f"{TOPIC_ROOT}/{sub_topic}",
                        table_name=None,
                        db_name=db_name,
                        payload=msg,
                        standalone_values=standalone_values,
                        loop=loop,
                    )

                    line_counts[idx] += 1
                    time.sleep(offset_sleep)

            else:
                # reset file when exhausted
                line_counts[idx] = 0

        counter += 1

        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)


def main(
    method: str,
    conn: RestClient | MqttClient | OpcuaServer | None,
    db_name: str,
    topic: str | List[str] | None = None,
    iterations: int = 10,
    sleep: float = 30,
    offset_sleep: float = 0.5,
    standalone_values: bool = False,
    loop=None,
):
    """
    Main entry point
    """

    topic_files = _extract_files(topic)

    threads = []

    for topic_name, files in topic_files.items():
        if not files:
            continue

        t = threading.Thread(
            target=_topic_worker,
            kwargs={
                "topic_name": topic_name,
                "files": files,
                "method": method,
                "conn": conn,
                "db_name": db_name,
                "iterations": iterations,
                "sleep": sleep,
                "offset_sleep": offset_sleep,
                "standalone_values": standalone_values,
                "loop": loop,
            },
            daemon=True,
        )

        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()


if __name__ == "__main__":
    main(
        method="PRINT",
        conn=None,
        db_name="",
        topic="Enterprise_C",
        iterations=5,
    )