import argparse
import datetime

import requests
import random
import json
from string import ascii_letters
from publisher_mqtt import publish_mqtt

def __extract_conn(conn_info:str)->(str, tuple):
    conns = {}
    for conn in conn_info.split(","):
        auth = ()
        if '@' in conn:
            auth, conn = conn.split('@')
            auth = tuple(auth.split(':'))
        conns[conn] = auth
    return conns


def get_columns(table_name:str):
    try:
        response = requests.get(url='http://23.239.12.151:32349',
                                headers={'command': f'get columns where dbms=cos and table={table_name} and format=json',
                                         'User-Agent': 'AnyLog/1.23'})
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"Failed to communicage against 23.239.12.151:32349 (Error: {error})")
    else:
        columns = response.json()
        for column in ['row_id', 'insert_timestamp', 'tsd_name', 'tsd_id', 'tsd_info']:
            if column in columns:
                del  columns[column]
    return columns

def data_generator(db_name:str, table_name:str, columns:str):
    payload = {'dbms': db_name, 'table': table_name}
    for column in columns:
        if 'int' == columns[column]:
            payload[column] = random.randint(1000, 10000)
        elif 'float' == columns[column]:
            payload[column] = random.random() * 1000
        elif 'decimal' == columns[column]:
            payload[column] = round(random.random() * 1000, 2)
        elif 'bool' in columns[column]:
            payload[column] = random.choice([True, False])
        elif 'timestamp' in columns[column]:
            payload[column] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        elif 'char' in columns[column]:
            payload[column] = ''
            for i in range(int(columns[column].split('(')[-1].split(')')[0])):
                payload[column] += random.choice(ascii_letters)

    return payload


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('conn',          type=str,   default=None, help='MQTT IP:Port')
    parse.add_argument('--db-name',     type=str,   default=None, help='logical database name')
    parse.add_argument('--max-size',    type=float, default=1.0, help='maximum size in MB')  # <-- CHANGED
    parse.add_argument('--size-type',   type=str,   default='MB', choices=['MB', 'GB', 'rows'], help='max size type')
    parse.add_argument('--batch-size',  type=int,   default=10, help='batch size')
    parse.add_argument('--qos',         type=int,   default=0,  choices=[0, 1, 2], help='Quality of serivce')
    parse.add_argument('--topic',       type=str,   default=None, help='MQTT topic')
    args = parse.parse_args()

    is_bool = True
    max_size = 0
    if args.size_type != 'rows':
        max_size = args.max_size * 1024 * 1024  # Convert MB to bytes
        if args.size_type == 'GB':
            max_size *= 1024 # Convert MB to GB to bytes

    conns = __extract_conn(conn_info=args.conn)
    tables = {}
    total_rows = 0
    total_size = 0
    payloads = []
    run_time =

    for table in ['pp_pm', 'wp_digital', 'wp_analog', 'wwp_digital', 'wwp_analog']:
        tables[table] = get_columns(table)

    while is_bool is True:
        conn = random.choice(list(conns.keys()))
        auth = conns[conn]
        table_name = random.choice(list(tables.keys()))

        payload = data_generator(db_name=args.db_name, table_name=table_name, columns=tables[table])
        payloads.append(payload)

        total_rows += len(payloads)
        total_size += sum(len(json.dumps(p).encode('utf-8')) for p in payloads)

        # Calculate total size of the payloads in bytes
        if len(payloads) == args.batch_size and ((args.size_type != 'rows' and total_size >= max_size) or (total_size >= max_size)) :
            print(payloads)  # Replace with MQTT call
            run_time += publish_mqtt(conn=conn, auth=auth, payload=payloads, topic=args.topic, qos=args.qos)
        if total_size >= max_size:
            is_bool = False

    if args.size_type == 'rows':
        print(f"Total Run Time: {run_time} | Total Rows: {total_rows} | Insert Rows/sec: {total_rows/run_time}")
    else:
        print(f"Total Run Time: {run_time} | Total Size: {total_size}{args.size_type} | Insert {args.size_type}/sec: {total_size / run_time}")


if __name__ == '__main__':
    main()