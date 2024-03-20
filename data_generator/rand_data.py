import random
from data_generator.support import create_timestamp


def data_generator(db_name:str='test'):
    return {
        "dbms": db_name,
        "table": "rand_data",
        "timestamp": create_timestamp(),
        "value": round(random.random() * random.choice(range(1, 1000)), 3)
    }
