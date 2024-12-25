import datetime
import json
import random
import string
import time
import uuid
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

data = {}

DESCRIBE_DATA = "describe_data.json"
NUM_WORKERS = 25  # Number of parallel threads


# -- describe data --
def describe_data():
    for table in range(25):
        data[f'table_{table + 1}'] = {}
        for column in ['timestamp', 'device_id', 'insert_id']:
            data[f'table_{table + 1}'][column] = {}
            if column == 'timestamp':
                data[f'table_{table + 1}'][column]['type'] = 'datetime'
            elif column == 'device_id':
                data[f'table_{table + 1}'][column]['value'] = uuid.uuid4().__str__()
            else:
                data[f'table_{table + 1}'][column]['type'] = 'string'
        for column in range(397):
            data[f'table_{table + 1}'][f'column_{column + 1}'] = {
                "type": random.choice(['string', 'bool', 'int', 'float'])
            }
            if data[f'table_{table + 1}'][f'column_{column + 1}']['type'] in ['int', 'float']:
                data[f'table_{table + 1}'][f'column_{column + 1}']['min'] = random.choice(list(range(1, 500)))
                data[f'table_{table + 1}'][f'column_{column + 1}']['max'] = random.choice(list(range(499, 1000)))
            elif data[f'table_{table + 1}'][f'column_{column + 1}']['type'] == 'string':
                data[f'table_{table + 1}'][f'column_{column + 1}']['length'] = random.choice(list(range(1, 10)))

    with open(DESCRIBE_DATA, 'w') as f:
        f.write(json.dumps(data, indent=4))


# -- describe data --

def read_description():
    with open(DESCRIBE_DATA, 'r') as f:
        return json.load(f)


def get_data(data_describe):
    output = {}
    for column in data_describe:
        if column == 'timestamp':
            output[column] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        elif column == 'device_id':
            output[column] = data_describe[column]['value']
        elif column == 'insert_id':
            output[column] = uuid.uuid4().__str__().replace("-", "")
        elif data_describe[column]['type'] == 'bool':
            output[column] = random.choice([True, False])
        elif data_describe[column]['type'] == 'int':
            output[column] = random.choice(list(range(data_describe[column]['min'], data_describe[column]['max'])))
        elif data_describe[column]['type'] == 'float':
            output[column] = round(random.random() * random.choice(
                list(range(data_describe[column]['min'], data_describe[column]['max']))), 3)
        elif data_describe[column]['type'] == 'string':
            value = ''.join(random.choice(string.ascii_letters) for _ in range(data_describe[column]['length']))
            if len(value) > data_describe[column]['length']:
                output[column] = value[data_describe[column]['length']-1:]


    return json.dumps(output)


def create_session():
    # Create a session with connection pooling and retries
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=50)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def put_data(conn:str, auth:tuple, dbms:str, table:str, payload:str, mode:str='streaming'):
    headers = {
        'type': 'json',
        'dbms': dbms,
        'table': table,
        'mode': mode,
        'Content-Type': 'text/plain'
    }
    try:
        r = requests.put(f'http://{conn}', auth=auth, timeout=30, headers=headers, data=payload)
    except Exception as e:
        raise Exception(f'Failed to send data via PUT against {conn} | table {table} (Error: {e})')
    else:
        if r.status_code != 200:
            raise Exception(f'Failed to send data via PUT against {conn} due to network error: {r.status_code}')


def put_data_with_session(session, conn: str, auth: tuple, dbms: str, table: str, payload: str,
                          mode: str = 'streaming') -> bool:
    headers = {
        'type': 'json',
        'dbms': dbms,
        'table': table,
        'mode': mode,
        'Content-Type': 'text/plain'
    }
    try:
        r = session.put(f'http://{conn}', auth=auth, timeout=30, headers=headers, data=payload)
    except Exception as e:
        raise Exception(f'Failed to send data via PUT against {conn} | table {table} (Error: {e})')
    else:
        if r.status_code != 200:
            raise Exception(f'Failed to send data via PUT against {conn} due to network error: {r.status_code}')
        return r


def worker(session, task):
    table, data_describe, conn, auth, dbms = task
    payload = get_data(data_describe)
    put_data_with_session(session, conn=conn, auth=auth, dbms=dbms, table=table, payload=payload, mode='streaming')


def main():
    data_describe = read_description()
    tasks = [
        (table, data_describe[table], '10.0.0.131:32149', (), 'nov')
        for table in data_describe
    ]

    # Create a session outside the thread pool
    session = create_session()

    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(worker, session, task) for task in tasks]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")


def main2():
    data_describe = read_description()
    for table in data_describe:
        payload = get_data(data_describe[table])
        put_data(conn='10.0.0.131:32149', auth=(), dbms='nov', table=table, payload=payload)
    time.sleep(0.5)

if __name__ == '__main__':
    print(datetime.datetime.now())
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
    while datetime.datetime.now() < end_time:
        main()
        time.sleep(0.5)
    print(datetime.datetime.now())
