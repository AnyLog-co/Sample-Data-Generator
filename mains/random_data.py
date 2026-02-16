import datetime
import json
import random
import time

def get_data(db_name:str="test"):
    """
    Generate random data
    """
    return {
        "dbms": db_name,
        "table": "rand_data",
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f'),
        "value": random.random()
    }


def main(method:str, conn, db_name:str="test", iterations:int=10, sleep:float=10):
    is_active = True
    counter = 0

    while is_active:
        payload = get_data(db_name=db_name)
        if method.upper() == "MQTT":
            conn.publish_data(topic="rand-data", payload=payload)
        else:
            headers = {
                **({
                   "type": "json",
                   "dbms": payload.get("dbms"),
                   "table": payload.get("table"),
                   "mode": "streaming"
                } if method.upper() == "PUT" else {}),
                **({
                    "command": "data",
                    "topic": "rand-data",
                } if method.upper() == "POST" else {}),
                "User-Agent": "AnyLog/1.23",
                "Content-Type": "text/plain"
            }
            if method.upper() == "POST":
                del payload["dbms"]
                del payload["table"]
            conn.publish_data(headers=headers, payload=json.dumps(payload), method=method.upper())

        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)