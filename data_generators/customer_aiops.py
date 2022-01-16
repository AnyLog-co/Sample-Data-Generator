import os
import random
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('data_generators', 1)[0]
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, PROTOCOLS)
from support import generate_timestamp

DATA_SETS = {
    "lic1_pv": {"min": -125, "max": 1522},
    "lic1_mv": {"min": 0, "max": 101},
    "fic11_mv": {"min": 64, "max": 77},
    "fic13_pv": {"min": 63, "max": 104},
    "fic11_pv": {"min": 48, "max": 103},
    "lic1_sv": {"min": 49, "max": 51},
    "fic12_pv": {"min": 41, "max": 96}
}


def get_aiops_data(timezone:str, sleep:float, repeat:int)->dict:
    """
    Generate values based on data from Ai-Ops
    :args:
        timezone:str - timezone for generated timestamp(s)
        sleep:float - wait time between each row
        repeat:int - number of times to repeat process
    :param:
        data_sets:dict - dict of data generated
    :return:
        data_sets
    """
    data_sets = {}
    for i in range(repeat):
        for table in DATA_SETS:
            if table not in data_sets:
                data_sets[table] = []
            data_sets[table].append({
                'timestamp': generate_timestamp(timezone=timezone),
                'value': random.random() + random.choice(range(DATA_SETS[table]['min'], DATA_SETS[table]['max']))
            })
        time.sleep(sleep)

    return data_sets