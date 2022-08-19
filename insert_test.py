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

import trig


def put_data(conn:str, payload:dict, dbms:str='test', table:str='rand_data'):
    json_payload = json.dumps(payload)
    headers = {
        'type': 'json',
        'dbms': dbms,
        'table': table,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }
    try:
        r = requests.put(url='http://%s' % conn, headers=headers, data=json_payload)
    except Exception as error:
        print(f'Failed to PUT data (Error: {error})')
    else:
        if int(r.status_code) != 200:
            print(f'Failed to PUT data (Error: {r.status_code})')


def insert_100k_24hrs(conns:list)->datetime.timedelta:
    """
    Insert 100k over 24 hour period
    :params:
        counter:int - number of rows inserted
        now:str - current timestamp (incremented by 0.864 seconds per insert)
        start:time.time - start timestamp
        process_time:float - sum of how long each insert took
    :return:
        epoch time of process_time
    """
    counter = 0
    now = datetime.datetime.utcnow()
    process_time = 0
    conns_counter = 0
    while counter < 100000:
        data_set = trig.trig_value(timezone='utc', enable_timezone_range=False, sleep=0, repeat=1)
        for section in data_set:
            for row in data_set[section]:
                conn = conns[conns_counter]
                row['timestamp'] = now.strftime('%Y-%m-%d %H:%M:%S.%f')
                start = time.time()
                put_data(conn=conn, payload=row, dbms='test', table='rand_data')
                process_time += (time.time() - start)
                now += datetime.timedelta(seconds=0.864)
                counter += 1
                conns_counter += 1
                if conns_counter == len(conns):
                    conns_counter = 0
    return datetime.timedelta(seconds=process_time)


def insert_1m_24hrs(conns:list)->datetime.timedelta:
    """
    Insert 100k over 24 hour period
    :params:
        counter:int - number of rows inserted
        now:str - current timestamp (incremented by 0.864 seconds per insert)
        start:time.time - start timestamp
        process_time:float - sum of how long each insert took
    :return:
        epoch time of process_time
    """
    counter = 0
    now = datetime.datetime.utcnow()
    process_time = 0
    conns_counter = 0
    while counter < 1000000:
        data_set = trig.trig_value(timezone='utc', enable_timezone_range=False, sleep=0, repeat=1)
        for section in data_set:
            for row in data_set[section]:
                conn = conns[conns_counter]
                row['timestamp'] = now.strftime('%Y-%m-%d %H:%M:%S.%f')
                start = time.time()
                print(conns, row)
                process_time += (time.time() - start)
                now += datetime.timedelta(seconds=0.0864)
                counter += 1
                conns_counter += 1
                if conns_counter == len(conns):
                    conns_counter = 0
    return datetime.timedelta(seconds=process_time)


if __name__ == '__main__':
    print(datetime.datetime.utcnow())
    print(insert_100k_24hrs(conns=['50.116.5.120:32149']))
    print(datetime.datetime.utcnow())