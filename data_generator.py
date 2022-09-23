"""
The following provides the ability to insert data into AnyLog

* Data Types
    -- performance test
    -- ping + percentagecpu sensor(s)
    -- opcu data
    -- solar panel data
    -- trig data
    -- read from file
* Insert Process
    -- PUT
    -- POST
    -- MQTT
    -- print
    -- to file
"""
import argparse
import datetime
import os
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
sys.path.insert(0, DATA_GENERATORS)

import lsl_data
import opcua_data
import performance_testing
import power_company
import timestamp_generator
import trig


def row_generator(data_type:str, db_name:str, array_counter:int=None)->dict:
    """
    Generate data to be inserted
    :args:
        data_type:str - type of data to insert into AnyLog
        db_name:str - logical database name
        array_counter:int - counter used in certain generators
    :params:
        payload:dict - content to storwe
    :return:
        payload
    """
    if data_type == 'trig': # {"timestamp", "sin", "cos", "trig"}
        payload = trig.trig_value(db_name=db_name, array_counter=array_counter)
        array_counter += 1
        if array_counter == len(trig.VALUE_ARRAY):
            array_counter = 0
    elif data_type == 'performance': # {"timestamp", "value"}
        payload = performance_testing.generate_row(db_name=db_name, array_counter=array_counter)
        array_counter += 1
        if array_counter == len(performance_testing.VALUE_ARRAY):
            array_counter = 0
    elif data_type == 'opcua':
        payload = opcua_data.get_opcua_data(db_name=db_name)
    elif data_type == 'percentagecpu':
        payload = lsl_data.percentagecpu_sensor(db_name=db_name)
    elif data_type == 'ping':
        payload = lsl_data.ping_sensor(db_name=db_name)
    elif data_type == 'power':
        payload = power_company.data_generator(db_name=db_name)

    return payload, array_counter


def include_timestamp(payload:dict, timezone:str='utc', enable_timezone_range:bool=False,
                      performance_testing:bool=False, base_timestamp:datetime.datetime=datetime.datetime.now(),
                      base_row_time:float=0, row_counter:int=0):
    """
    Generate timestamp for row - if performance testing is enabled, timestamps within will be within a 24 hour period.
    :args:
       payload:dict - row(s) to add timestamp for
       timezone:str - timezone for generated timestamp(s)
       enable_timezone_range:bool - whether or not to set timestamp within a "range"
       performance_testing:bool - insert all rows within a 24 hour period (if enabled, timezone params are ignored)
       base_timestamp:datetime.datetime - initial timestamp for performance testing
       base_row_time:float - timestamp incremental value for performance testing
       row_counter:int - current row -- ueed in calculating timestamp for performance
    :params:
        timestamp:str - calculated timestamp (as string)
    :return:
        updated payload
    """
    timestamp = timestamp_generator.generate_timestamp(timezone=timezone, enable_timezone_range=enable_timezone_range)
    if performance_testing is True:
        timestamp = timestamp_generator.performance_timestamps(timestamp=base_timestamp, base_timestamp=base_row_time,
                                                               row_counter=row_counter)
    if isinstance(payload, dict):
        payload['timestamp'] = timestamp
    else:
        for i in range(payload):
            payload[i]['timestamp'] = timestamp

    return payload


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('data_type', type=str, choices=['trig', 'performance', 'ping', 'percentagecpu', 'opcua', 'power'],
                       default='trig', help='type of data to insert into AnyLog')
    parse.add_argument('insert_process', type=str, choices=['print', 'file', 'put', 'post', 'mqtt'],
                       default='print', help='format to store generated data')
    parse.add_argument('db_name', type=str, default='test', help='logical database name')
    parse.add_argument('--total-rows', type=int, default=1000000,
                       help='number of rows to insert. If set to 0, will run continuously')
    parse.add_argument('--batch-size', type=int, default=1000, help='number of rows to insert per iteration')
    parse.add_argument('--sleep', type=float, default=0.5, help='wait time between each row')
    parse.add_argument('--timezone', type=str, choices=['local', 'UTC', 'ET', 'BR', 'JP', 'WS', 'AU', 'IT'],
                       default='local', help='timezone for generated timestamp(s)')
    parse.add_argument('--enable-timezone-range', type=bool, nargs='?', const=True, default=False,
                       help='whether or not to set timestamp within a "range"')
    parse.add_argument('--conn', type=str, default=None,
                       help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parse.add_argument('--rest-timeout', type=float, default=30, help='')
    parse.add_argument('--dir-name', type=str, default=DATA_DIR, help='directory when storing to file')
    parse.add_argument('--performance-testing', type=bool, nargs='?', const=True, default=False,
                       help='insert all rows within a 24 hour period')
    args = parse.parse_args()

    total_row = args.total_rows
    array_counter = 0
    row_counter = 0
    data = []
    conns = {}

    if args.conn is not None:
        for conn in args.conn.split(','):
            if '@' in conn:
                conns[conn.split('@')[-1]] = conn.split('@')[0]
            else:
                conns[conn.split('@')[-1]] = None

    if args.performance_testing is True:
        start_timestamp = timestamp_generator.performance_start_timestamp()
        base_row_time = timestamp_generator.base_row_time(total_rows=total_rows)
        if total_rows == 0:
            total_rows = 1000000
        for row_counter in range(total_rows):
            payload, array_counter, = row_generator(data_type=args.data_type, db_name=args.db_name,
                                                    array_counter=array_counter)
            payload = include_timestamp(payload=payload, performance_testing=True, base_timestamp=start_timestamp,
                                        base_row_time=base_row_time, row_counter=row_counter)
            if instance(payload, dict):
                data.append(payload)
            else:
                data += payload
            row_counter += 1
            if row_counter == args.batch_size:
                # send data
                data = []
                row_counter = 0
            time.sleep(args.sleep)

    elif total_row != 0:
        for row_counter in range(total_rows):
            payload, array_counter, = row_generator(data_type=args.data_type, db_name=args.db_name,
                                                    array_counter=array_counter)
            payload = include_timestamp(payload=payload, timezone=args.timezone,
                                        enable_timezone_range=enable_timezone_range, performance_testing=False)
            # once batch is full - insert data
    else:
        while True:
            payload, array_counter, = row_generator(data_type=args.data_type, db_name=args.db_name,
                                                    array_counter=array_counter)
            payload = include_timestamp(payload=payload, timezone=args.timezone,
                                        enable_timezone_range=enable_timezone_range, performance_testing=False)
            # once batch is full - insert data


if __name__ == '__main__':
    main()

