import posixpath
import time
from typing import Dict, List
import copy

from source.southbound.support import get_files_by_url, url_read_content
from source.northbound.support import publish_data
from source.northbound.rest_calls import RestClient
from source.northbound.mqtt import MqttClient
from source.northbound.opcua import OpcuaServer

DATA_DIR = "http://45.33.11.32/Sample-Data/proveit-data2/"
ALL_FILES = get_files_by_url(url=DATA_DIR)

TOPIC_ROOT = "proveit"


def _check_topics(topics: str | List[str] | None = None) -> Dict[str, List[str]]:
    """
    Validate and group files by topic
    """
    if isinstance(topics, str):
        topics = topics.split(",")

    topics = topics or ["Enterprise_A", "Enterprise_B", "Enterprise_C"]

    topic_files = {topic: [] for topic in topics}

    for fname in ALL_FILES:
        for topic in topics:
            if fname.startswith(topic):
                topic_files[topic].append(fname)

    if not any(topic_files.values()):
        raise Exception("No matching files found for provided topics")

    return topic_files


def main(
    method: str,
    conn: RestClient | MqttClient | OpcuaServer | None,
    db_name: str,
    publish_topics: str | List[str] | None = None,
    iterations: int = 10,
    sleep: float = 10,
    offset_sleep: float = 0.5,
    standalone_values: bool = False,
    loop=None,
):
    """
    Main loop for publishing proveit data (rig-style behavior)
    """

    topic_files = _check_topics(topics=publish_topics)

    # Build full paths
    topic_paths: Dict[str, List[str]] = {
        topic: [posixpath.join(DATA_DIR, f) for f in files]
        for topic, files in topic_files.items()
    }

    # Track state per topic + file
    line_counts = {
        topic: [
            {"line_num": 0}
            for _ in files
        ]
        for topic, files in topic_paths.items()
    }

    counter = 0
    is_active = True

    while is_active:
        for topic, files in topic_paths.items():

            for idx, file_path in enumerate(files):
                state = line_counts[topic][idx]

                row = url_read_content(file_path, line=state["line_num"])

                if row:
                    msg = row.get("msg")
                    sub_topic = row.get("topic") or topic

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

                        state["line_num"] += 1
                        time.sleep(offset_sleep)

                else:
                    # reset file when exhausted
                    state["line_num"] = 0

        counter += 1

        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)


if __name__ == "__main__":
    main(
        method="PRINT",
        conn=None,
        db_name="",
        publish_topics="Enterprise_C",
        iterations=5,
    )