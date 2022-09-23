import argparse
import datetime
import json
import os
import random
import requests
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PROTOCOLS)

# base timestamp 2022-08-27 15:50:12
START_TIMESTAMP = datetime.datetime(year=2022, month=8, day=27, hour=15, minute=50, second=12) + datetime.timedelta(microseconds=random.choice(range(100, 300000)))
SECOND_INCREMENTS = 0.864
ROWS_24h_INCREMENTS = 100000


VALUE_ARRAY = [ # 90
    -1.2246467991473532e-16, -1.0, 1.2246467991473532e-16, -1.0, 6.123233995736766e-17, -1.633123935319537e+16,
    -0.8660254037844386, 0.5000000000000001, -1.7320508075688767, -0.8414709848078965, 0.5403023058681398,
    -1.557407724654902, -0.7071067811865475, 0.7071067811865476, -0.9999999999999999, -0.49999999999999994,
    0.8660254037844387, -0.5773502691896256, -0.3826834323650898, 0.9238795325112867, -0.4142135623730951, 0.0, 1.0,
    0.0, 0.3826834323650898, 0.9238795325112867, 0.4142135623730951, 0.49999999999999994, 0.8660254037844387,
    0.5773502691896256, 0.7071067811865475, 0.7071067811865476, 0.9999999999999999, 0.8414709848078965,
    0.5403023058681398, 1.557407724654902, 0.8660254037844386, 0.5000000000000001, 1.7320508075688767, 1.0,
    6.123233995736766e-17, 1.633123935319537e+16, 1.2246467991473532e-16, -1.0, -1.2246467991473532e-16,
    1.2246467991473532e-16, -1.0, -1.2246467991473532e-16, 1.0, 6.123233995736766e-17, 1.633123935319537e+16,
    0.8660254037844386, 0.5000000000000001, 1.7320508075688767, 0.8414709848078965, 0.5403023058681398,
    1.557407724654902, 0.7071067811865475, 0.7071067811865476, 0.9999999999999999, 0.49999999999999994,
    0.8660254037844387, 0.5773502691896256, 0.3826834323650898, 0.9238795325112867, 0.4142135623730951,
    0.0, 1.0, 0.0, -0.3826834323650898, 0.9238795325112867, -0.4142135623730951, -0.49999999999999994,
    0.8660254037844387, -0.5773502691896256, -0.7071067811865475, 0.7071067811865476, -0.9999999999999999,
    -0.8414709848078965, 0.5403023058681398, -1.557407724654902, -0.8660254037844386, 0.5000000000000001,
    -1.7320508075688767, -1.0, 6.123233995736766e-17, -1.633123935319537e+16, -1.2246467991473532e-16, -1.0,
    1.2246467991473532e-16
]


def generate_row(db_name:str, array_counter:int)->dict:
    """
    Generate row to be inserted
    :args:
        db_name:str - logical database name
        array_counter:int - placeholder in VALUE_ARRAY
    :params:
        row_value:float - trig calculation based on value
            - if row_counter % 10 - use tangent
            - if row_counter % 2 - use sine
            - else - use cosine
        seconds:float - increments size
        now:datetime.datetime - row timestamp
        row:dict - {timestamp, value} object to store in operator
    :return:
        row
    """
    row = {
        'dbms': db_name,
        'table': 'rand_data',
        'value': VALUE_ARRAY[array_counter]
    }

    return row


if __name__ == '__main__':
    main()

