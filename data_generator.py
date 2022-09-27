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
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import support

import generic_protocol
import mqtt_protocol
import rest_protocols

import lsl_data
import opcua_data
import performance_testing
import power_company
import timestamp_generator
import trig

DATA_DIR = os.path.join(ROOT_PATH, 'data')

def __rows_summary(db_name:str)->str:
    """
    The following provides an example for each of the data types, printing them to screen
    :args:
        db_name:str - logical database name
    :params:
        payloads:dict - sample data
    """
    payloads = {
        'trig': {'dbms': db_name, 'table': 'trig_data', 'value': -3.141592653589793, 'sin': -1.2246467991473532e-16,
                 'cos': -1.0, 'tan': 1.2246467991473532e-16, 'timestamp': '2022-08-27T15:50:12.001399Z'},
        'performance': {'dbms': db_name, 'table': 'rand_data', 'value': -1.2246467991473532e-16,
                        'timestamp': '2022-08-27T15:50:12.163818Z'},
        'ping': {'dbms': db_name, 'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT',
                 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba',
                 'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw',
                 'value': 44.74, 'timestamp': '2022-08-27T15:50:12.059726Z'},
        'percentagecpu': {'dbms': db_name, 'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS',
                          'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba',
                          'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H',
                          'value': 9.59, 'timestamp': '2022-08-27T15:50:12.116925Z'},
        'opcua': {"dbms": "test2", "table": "opcua_readings", "fic1_pv": -103.29249139515318, "fic1_mv": -227.862187363,
                  "fic1_sv": -48.493873977761645, "lic1_pv": 165.18648883311027, "lic1_mv": -84.59834643031611,
                  "lic1_sv": 174.86936425992465, "fic2_pv": -37.52888216655371, "fic2_mv": 38.63696693385969,
                  "fic2_sv": -182.07962937349504, "lic2_pv": 142.90402691921074, "lic2_mv": -35.64751556177472,
                  "lic2_sv": -62.69296482664739, "fic3_pv": -147.060548270305, "fic3_mv": -57.93928389193016,
                  "fic3_sv": 418.2631932904929, "lic3_pv": 176.7756420678825, "lic3_mv": -61.49695028678772,
                  "lic3_sv": 220.60063882032966, "fic4_pv": -44.66240442407483, "fic4_mv": 11.529102739194443,
                  "fic4_sv": 124.97175098185224, "lic4_pv": 9.507763915723592, "lic4_mv": 30.483647656168543,
                  "lic4_sv": -213.4404433100362, "fic5_pv": -460.10226426203155, "fic5_mv": -72.96099747863087,
                  "fic5_sv": -53.62672940378895, "lic5_pv": -89.93465024402398, "lic5_mv": -20.523831049180885,
                  "lic5_sv": -125.29010564894106, "timestamp": "2022-09-24T14:30:10.575429Z"},
        'power': [
            {'dbms': db_name, 'table': 'solar', 'location': '38.89773, -77.03653', 'value': 8.43453536493608,
             'timestamp': '2022-08-27T15:50:12.205323Z'},
            {'dbms': db_name, 'table': 'battery', 'location': '38.89773, -77.03653', 'value': 9.532695799656166,
             'timestamp': '2022-08-27T15:50:12.205323Z'},
            {'dbms': db_name, 'table': 'inverter', 'location': '38.89773, -77.03653', 'value': 20.03601934228979,
             'timestamp': '2022-08-27T15:50:12.205323Z'},
            {'dbms': db_name, 'table': 'eswitch', 'location': '38.89773, -77.03653', 'value': 9.530111494215165,
             'timestamp': '2022-08-27T15:50:12.205323Z'},
            {'dbms': db_name, 'table': 'pmu', 'location': '38.89773, -77.03653', 'value': 30.51712172789563,
             'timestamp': '2022-08-27T15:50:12.205323Z'},
            {'dbms': db_name, 'table': 'synchrophasor', 'location': '38.89773, -77.03653', 'phasor': 'bXlvzdYc',
             'frequency': 1216.6996978149687, 'dfreq': 2326.468559576384, 'analog': 4.591088473171304,
             'timestamp': '2022-08-27T15:50:12.205323Z'}
        ]
    }

    for table in payloads:
        print(f'Data Type: {table}')
        if isinstance(payloads[table], list):
            for payload in payloads[table]:
                print(f'\t{support.json_dumps(payload)}')
        else:
            print(f'\t{support.json_dumps(payloads[table])}')
        print('\n')


def row_generator(data_type:str, db_name:str, array_counter:int=None)->(dict, int):
    """
    Generate data to be inserted
    :args:
        data_type:str - type of data to insert into AnyLog
        db_name:str - logical database name
        array_counter:int - counter used in certain generators
    :params:
        payload:dict - content to storwe
    :return:
        payload + array_counter
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
        timestamp = timestamp_generator.performance_timestamps(timestamp=base_timestamp, base_row_time=base_row_time,
                                                               row_counter=row_counter)
    if isinstance(payload, dict):
        payload['timestamp'] = timestamp
    else:
        for i in range(len(payload)):
            payload[i]['timestamp'] = timestamp

    return payload


def publish_data(payload:list, insert_process:str, conn:str=None, topic:str=None, rest_timeout:int=30,
                 dir_name:str=None, compress:bool=False, exception:bool=False):
    """
    Publish data based on the insert_process
    :args:
        payload:list - content to store
        insert_process:str - format to store content in
        conn:str - connection information
        topic:str - REST POST + MQTT topic
        rest_timeout:int - REST timeout
        dir_name:str - directory to store files in
        compress:bool - whether to compress content or not when stored in file
        exception:bool - whether to print error message(s)
    :params:
        status:bool
    """
    auth = ()
    if insert_process in ['put', 'post', 'mqtt']:
        if '@' in conn:
            auth, conn = conn.split('@')
            auth = tuple(auth.split(':'))

    if insert_process == "print":
        generic_protocol.print_content(payloads=payload)
    elif insert_process == "file":
        status = generic_protocol.write_to_file(payloads=payload, data_dir=dir_name, compress=compress, exception=exception)
        if status is False and exception is False:
            print(f'Failed to store content into file')
        elif insert_process == 'put':
            status = rest_protocolss.put_data(payloads=payload, conn=conn, auth=auth, timeout=rest_timeout,
                                             exception=exception)
            if status is False and exception is False:
                print(f'Failed to insert one or more batches of data into {conn} via PUT')
    elif insert_process == 'post':
        status = rest_protocolss.post_data(payloads=payload, topic=topic, conn=conn, auth=auth, timeout=rest_timeout,
                                          exception=exception)
        if status is False and exception is False:
            print(f'Failed to insert one or more batches of data into {conn} via POST')
    elif insert_process == 'mqtt':
        broker, port = conn.split(':')
        username = ""
        password = ""
        if auth != ():
            username, password = auth

        status = mqtt_protocol.mqtt_process(payloads=payload, topic=topic, broker=broker, port=port, username=username,
                                            password=password, exception=exception)
        if status is False and exception is False:
            print(f'Failed to send MQTT message against connection {conn}')


def main():
    """
    :positional arguments::
        data_type           DATA_TYPE           type of data to insert into AnyLog          [default: trig]
            * trig
            * performance
            * ping
            * percentagecpu
            * opcua
            * power
            * examples - sample row(s) for each datta type
        insert_process      INSERT_PROCESS      format to store generated data              [default: print]
            * print
            * file
            * put
            * post
            * mqtt
        db_name             DB_NAME             logical database name                       [default: test]
    :optional arguments:
        -h, --help            show this help message and exit
        --total-rows    TOTAL_ROWS      number of rows to insert. If set to 0, will run continuously    [default: 1000000]
        --batch-size    BATCH_SIZE      number of rows to insert per iteration      [default: 1000]
        --sleep         SLEEP           wait time between each row                  [default: 0.5]
        --timezone      TIMEZONE        timezone for generated timestamp(s)         [default: utc | options: local,UTC,ET,BR,JP,WS,AU,IT]
        --enable-timezone-range     [ENABLE_TIMEZONE_RANGE]       set timestamp within a range of +/- 1 month
        --performance-testing   [PERFORMANCE_TESTING]     insert all rows within a 24 hour period
        --conn      CONN           {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        --topic     TOPIC          topic for publishing data via REST POST or MQTT
        --rest-timeout  REST_TIMEOUT    how long to wait before stopping REST       [default: 30]
        --dir-name      DIR_NAME        directory when storing to file
        --compress      [COMPRESS]      whether to zip data dir
        --exception     [EXCEPTION]     whether to print exceptions
    :params:
        total_rows:int - total number of rows (based on args.total_rows)
        array_counter:int - placeholder for values in certain data set(s)
        row_counter:int - number of rows inserted
        data:list - list of data to be stored
        conns:list - list of connection information
        conn_id:int - location along the
    """
    parse = argparse.ArgumentParser()
    parse.add_argument('data_type', type=str, choices=['trig', 'performance', 'ping', 'percentagecpu', 'opcua', 'power',
                                                       'examples'], default='trig',
                       help='type of data to insert into AnyLog')
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
                       help='set timestamp within a range of +/- 1 month')
    parse.add_argument('--performance-testing', type=bool, nargs='?', const=True, default=False,
                       help='insert all rows within a 24 hour period')
    parse.add_argument('--conn', type=str, default=None,
                       help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parse.add_argument('--topic', type=str, default=None, help='topic for publishing data via REST POST or MQTT')
    parse.add_argument('--rest-timeout', type=float, default=30, help='how long to wait before stopping REST')
    parse.add_argument('--dir-name', type=str, default=DATA_DIR, help='directory when storing to file')
    parse.add_argument('--compress', type=bool, nargs='?', const=True, default=False, help='whether to zip data dir')
    parse.add_argument('--exception', type=bool, nargs='?', const=True, default=False, help='whether to print exceptions')
    args = parse.parse_args()

    total_rows = args.total_rows
    array_counter = 0
    row_counter = 0
    data = []

    if args.data_type == 'examples':
        __rows_summary(db_name=args.db_name)
        exit(1)

    conns = None
    conn = None
    conn_id = 0
    if args.conn is not None:
        conns = args.conn.split(',')

    if args.performance_testing is True:
        start_timestamp = timestamp_generator.performance_start_timestamp()
        base_row_time = timestamp_generator.base_row_time(total_rows=total_rows)
        if total_rows == 0:
            total_rows = 1000000
        for row in range(total_rows):
            payload, array_counter, = row_generator(data_type=args.data_type, db_name=args.db_name,
                                                    array_counter=array_counter)
            payload = include_timestamp(payload=payload, performance_testing=True, base_timestamp=start_timestamp,
                                        base_row_time=base_row_time, row_counter=row_counter)
            if isinstance(payload, dict):
                data.append(payload)
            else:
                data += payload
            row_counter += 1
            if row_counter == args.batch_size:
                if conns is not None:
                    conn = conns[conn_id]
                publish_data(payload=data, insert_process=args.insert_process, conn=conn,
                             rest_timeout=args.rest_timeout, dir_name=args.dir_name)
                data = []
                row_counter = 0
                if conns is not None:
                    conn_id += 1
                    if conn_id == len(conns):
                        conn_id = 0
            time.sleep(args.sleep)
        if len(data) > 0:
            if conns is not None:
                conn = conns[conn_id]
            publish_data(payload=data, insert_process=args.insert_process, conn=conn,
                         rest_timeout=args.rest_timeout, dir_name=args.dir_name)
    elif total_rows != 0:
        for row in range(total_rows):
            payload, array_counter, = row_generator(data_type=args.data_type, db_name=args.db_name,
                                                    array_counter=array_counter)
            payload = include_timestamp(payload=payload, timezone=args.timezone,
                                        enable_timezone_range=args.enable_timezone_range, performance_testing=False)
            if isinstance(payload, dict):
                data.append(payload)
            else:
                data += payload
            row_counter += 1
            if row_counter == args.batch_size:
                if conns is not None:
                    conn = conns[conn_id]
                publish_data(payload=data, insert_process=args.insert_process, conn=conn,
                             rest_timeout=args.rest_timeout, dir_name=args.dir_name)
                data = []
                row_counter = 0
                if conns is not None:
                    conn_id += 1
                    if conn_id == len(conns):
                        conn_id = 0
            time.sleep(args.sleep)
        if len(data) > 0:
            if conns is not None:
                conn = conns[conn_id]
            publish_data(payload=data, insert_process=args.insert_process, conn=conn,
                         rest_timeout=args.rest_timeout, dir_name=args.dir_name)
    else:
        while True:
            payload, array_counter, = row_generator(data_type=args.data_type, db_name=args.db_name,
                                                    array_counter=array_counter)
            payload = include_timestamp(payload=payload, timezone=args.timezone,
                                        enable_timezone_range=enable_timezone_range, performance_testing=False)
            if isinstance(payload, dict):
                data.append(payload)
            else:
                data += payload
            row_counter += 1
            if row_counter == args.batch_size:
                if conns is not None:
                    conn = conns[conn_id]
                publish_data(payload=data, insert_process=args.insert_process, conn=conn,
                             rest_timeout=args.rest_timeout, dir_name=args.dir_name)
                data = []
                row_counter = 0
                if conns is not None:
                    conn_id += 1
                    if conn_id == len(conns):
                        conn_id = 0
            time.sleep(args.sleep)


if __name__ == '__main__':
    main()

