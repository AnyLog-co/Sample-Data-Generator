import random
import time

from source.northbound.support import publish_data
from source.southbound.support import calculate_timestamp

TABLE = "rand_data"
TOPIC = "rand-data"

def get_data():
    """
    Generate random data
    """
    return {
        "timestamp": calculate_timestamp(row_id=0, off_set=0, current_timestamp=None),
        "value": random.random()
    }


def main(method:str, conn, db_name:str="test", iterations:int=10, sleep:float=10, standalone_value:bool=False,
         loop=None):
    is_active = True
    counter = 0

    while is_active:
        payload = get_data()
        if method in ["MQTT", "POST", "KAFKA"]:
            payload.update({
                "dbms": db_name,
                "table": TABLE,
            })
        publish_data(method=method, conn=conn, topic=TOPIC, table_name=TABLE, db_name=db_name, payload=payload,
                     standalone_values=standalone_value, loop=loop)


        counter += 1
        if iterations > 0 and  0 < iterations <= counter:
            is_active = False
        else:
            time.sleep(sleep)

