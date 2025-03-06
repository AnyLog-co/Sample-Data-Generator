import random
from random import choice

from data_generator.support import create_timestamp


def data_generator(db_name:str='test', is_aggregated:bool=False, last_value:float=None, tolerance_level:float=0):
    """
    Generate random value
    """
    if is_aggregated is True:
        if last_value is None:
            last_value = round(random.random() * random.choice(range(1, 1000)), 3)
        if 0 < tolerance_level < 1:
            value = random.uniform(last_value * (1 - tolerance_level), last_value * (1 + tolerance_level))
        elif tolerance_level > 1:
            value = random.uniform(last_value * (1 - (tolerance_level/100)), last_value * (1 + (tolerance_level/100)))
        else:
            value = last_value
    else:
        last_value, value = None, round(random.random() * random.choice(range(1, 1000)), 3)

    data = {
        "dbms": db_name,
        "table": "rand_data",
        "timestamp": create_timestamp(),
        "value": value
    }
    return data, last_value
