import posixpath
from source.northbound.rest_functions import declare_msg_client
from source.northbound.rest_calls import RestClient

TOPIC = "wind-turbine2"

def run_msg_client(conn:RestClient|None, broker:str, port:int, is_rest:bool=False, db_name:str="wind_turbine",
                   turbine_id:list[str]|str|None=None):
    topic = f"(name=%s and dbms={db_name} and dynamic=True)"

    if turbine_id == '#' or turbine_id is None:
        declare_msg_client(conn=conn, broker=broker, port=port, is_rest=is_rest, topics=topic %  TOPIC)
    elif turbine_id is not None and isinstance(turbine_id, str):
        turbine_ids = turbine_id.split(",")
        topics = ""
        for turbine_id in turbine_ids:
            sub_topic = posixpath.join(TOPIC, turbine_id.rsplit('/')[0].strip() if topic.endswith('/#') else topic.strip())
            topics += topic % sub_topic
        topics = topics.rsplit(" and ").strip()
        declare_msg_client(conn=conn, broker=broker, port=port, is_rest=is_rest, topics=topics)


def enable_streamer(conn:RestClient|None):
    headers = {
        "command": "run uns streamer",
        "User-Agent": "AnyLog/1.23"
    }
    conn.publish_data(headers=headers, payload=None, method="POST")


# if __name__ == "__main__":
#     main()
