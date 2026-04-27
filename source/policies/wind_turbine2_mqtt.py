import posixpath
from source.northbound.rest_functions import declare_msg_client
from source.northbound.rest_calls import RestClient

TOPIC = "wind-turbine2"

def run_msg_client(conn:RestClient|None, broker:str, port:int, is_rest:bool=False, db_name:str="wind_turbine",
                   turbine_id:list[str]|str|None=None):
    topic = f"(name=%s and dbms={db_name} and dynamic=True and column.timestamp.timestamp=now())"
    turbine_ids = turbine_id
    turbine_topics = []
    if turbine_id not in [None, '#'] and isinstance(turbine_id, str):
        turbine_ids = turbine_id.split(",")

    if turbine_id in [None, '#']:
        turbine_topics.append(topic %  TOPIC)
    else:
        for turbine_id in turbine_ids:
            sub_topic = posixpath.join(TOPIC, turbine_id)
            if not sub_topic.endswith("/#"):
                sub_topic = posixpath.join(sub_topic, '#')
            turbine_topics.append(topic % sub_topic)

    declare_msg_client(conn=conn, broker=broker, port=port, is_rest=is_rest, topics=turbine_topics)

def enable_streamer(conn:RestClient|None):
    headers = {
        "command": "run uns streamer",
        "User-Agent": "AnyLog/1.23"
    }
    conn.publish_data(headers=headers, payload=None, method="POST")


# if __name__ == "__main__":
#     main()
