import datetime
import json
import random
import time

from source.northbound.publish_data import publish_data

TABLE = "rand_data"
TOPIC = "rand-data"

def get_data():
    """
    Generate random data
    """
    return {
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f'),
        "value": random.random()
    }


def main(method:str, conn, db_name:str="test", iterations:int=10, sleep:float=10):
    is_active = True
    counter = 0

    while is_active:
        payload = get_data()
        if method in ["MQTT", "POST"]:
            payload.update({
                "dbms": db_name,
                "table": TABLE,
            })
        publish_data(method=method, conn=conn, topic=TOPIC, table_name=TABLE, db_name=db_name, payload=payload)

        counter += 1
        if 0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)