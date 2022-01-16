import os
import random
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('data_generators', 1)[0]
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, PROTOCOLS)
from support import generate_timestamp

LOCATIONS = [
    '33.8121, -117.91899', # LA
    '37.786163522 -122.404498382', # SF
    '47.620182, -122.34933', # Seattle
    '39.949566, -75.15026', # Phili
    '38.870983,  -77.05598', # Arlington
    '38.89773, -77.03653', # DC
    '40.758595, -73.98447', # NYC
    '28.37128, -81.51216' # Orlando 
    '29.97980499267578, -95.56627655029297', # Houston
    '36.1147, -115.1728' # Las Vegas
]

DATA = {
    'solar': [5, 50],    # Solar controller
    'battery': [5, 50],  # Battery controller
    'inverter': [5, 50], # Inverter controller
    'eswitch': [5, 50],  # Electric Switch controller
    'pmu': [5, 50]
}

def __calculate_value(val_range:list)->float:
    """
    Calculate a random value within a given range
    :args:
        val_range:list - range between 2 values
    :params:
        base_float:int - random value within val_range
        float_value:int - base_value * random.random()
    :return:
        float value within range
    """
    base_value = random.randrange(val_range[0], val_range[1])
    float_value = random.random() * base_value

    if val_range[0] < float_value + base_value < val_range[1]:
        return float_value + base_value
    elif val_range[0] < float_value < val_range[1]:
        return float_value
    elif val_range[0] + float_value < val_range[1]:
        return val_range[0] + float_value
    elif val_range[1] - float_value < val_range[0]:
        return val_range[1] - float_value
    else:
        return float_value - random.random()


def data_generator(timezone:str, enable_timezone_range:bool, sleep:float, repeat:int)->dict:
    """
    Generate data for non-synchorphiser table
    :args:
        timezone:str - timezone for generated timestamp(s)
        sleep:float - wait time between each row
        repeat:int - number of times to repeat
    :params:
        payloads:dict - dictionary of data
    :return:
        payloads
    """
    payloads = {}

    for i in range(repeat):
        timestamp = generate_timestamp(timezone=timezone, enable_timezone_range=enable_timezone_range)
        for table in list(DATA.keys()):
            if table not in payloads:
                payloads[table] = []
            location = random.choice(LOCATIONS)
            if len(location.split(',')) == 3:
                location = location.rsplit(',', 1)[0]
            payloads[table].append({
                'timestamp': timestamp,
                'location': location,
                'value': __calculate_value(DATA[table])
            })
            time.sleep(sleep)

    return payloads


if __name__ == '__main__':
    print(data_generator(sleep=0.5, repeat=10))