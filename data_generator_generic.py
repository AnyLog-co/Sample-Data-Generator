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
import random
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import publishing_protocols.support as support
import publishing_protocols.publish_data as publish_data

import data_generators.lsl_data as lsl_data
import data_generators.opcua_data as opcua_data
import data_generators.performance_testing as performance_testing
import data_generators.power_company as power_company
import data_generators.timestamp_generator as timestamp_generator
import data_generators.trig as trig

DATA_DIR = os.path.join(ROOT_PATH, 'data')
MICROSECONDS = random.choice(range(100, 300000)) # initial microseconds for timestamp value
SECOND_INCREMENTS = 86400  # second increments (0.864) for 100000 rows


def __row_size(arg):
    try:
        value = int(arg)
    except Exception as error:
        output = argparse.ArgumentTypeError(f"User input value {arg} is not of type integer (Error: {error})")
    else:
        if value < 0:
            output = argparse.ArgumentTypeError(f"User input value must be greater or equal to 0")
        else:
            output = value

    return output


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
                      performance_testing:bool=False, microseconds:int=MICROSECONDS, second_increments:float=0):
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
        timestamp = timestamp_generator.performance_timestamp(microseconds=microseconds, second_increments=second_increments)

    if isinstance(payload, dict):
        payload['timestamp'] = timestamp
    else:
        for i in range(len(payload)):
            payload[i]['timestamp'] = timestamp

    return payload



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
    parse.add_argument('--table-name', type=str, default=None,
                       help='Change default table name (valid for data_types except power)')
    parse.add_argument('--total-rows', type=__row_size, default=1000000,
                       help='number of rows to insert. If set to 0, will run continuously')
    parse.add_argument('--batch-size', type=__row_size, default=10, help='number of rows to insert per iteration')
    parse.add_argument('--sleep', type=float, default=0.5, help='wait time between each row')
    parse.add_argument('--timezone', type=str, choices=['local', 'utc', 'et', 'br', 'jp', 'ws', 'au', 'it'],
                       default='local', help='timezone for generated timestamp(s)')
    parse.add_argument('--enable-timezone-range', type=bool, nargs='?', const=True, default=False,
                       help='set timestamp within a range of +/- 1 month')
    parse.add_argument('--performance-testing', type=bool, nargs='?', const=True, default=False,
                       help='insert all rows within a 24 hour period')
    parse.add_argument('--conn', type=str, default=None,
                       help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parse.add_argument('--topic', type=str, default=None, help='topic for publishing data via REST POST or MQTT')
    parse.add_argument('--rest-timeout', type=float, default=30, help='how long to wait before stopping REST')
    parse.add_argument('--qos', type=int, choice=list(range(0, 4)), default=0, help='MQTT Quality of Service')
    parse.add_argument('--dir-name', type=str, default=DATA_DIR, help='directory when storing to file')
    parse.add_argument('--compress', type=bool, nargs='?', const=True, default=False, help='whether to zip data dir')
    parse.add_argument('--exception', type=bool, nargs='?', const=True, default=False, help='whether to print exceptions')
    args = parse.parse_args()

    total_rows = args.total_rows
    if args.batch_size <= 0:
        args.batch_size = 1
    array_counter = 0
    data = []

    if args.data_type == 'examples':
        __rows_summary(db_name=args.db_name)
        exit(1)

    conns = None
    if args.conn is not None:
        conns = args.conn.split(',')

    if args.insert_process == "mqtt":
        conns = publish_data.connect_mqtt(conns, exception=args.exception)
        if not conns:
            print("Failed to set connection for MQTT publisher")
            exit(1)
    elif args.insert_process in ["post", "put"]:
        conns = publish_data.setup_put_post_conn(conns=conns)

    if args.performance_testing is True:
        if total_rows == 0:
            total_rows = 1000000
        second_increments = 0 * (SECOND_INCREMENTS / args.total_rows)

    if total_rows > 0:
        for row in range(total_rows):
            payload, array_counter, = row_generator(data_type=args.data_type, db_name=args.db_name,
                                                    array_counter=array_counter)
            if args.performance_testing is True:
                payload = include_timestamp(payload=payload, performance_testing=True, microseconds=MICROSECONDS,
                                            second_increments=second_increments)
                second_increments = (row + 1) * (SECOND_INCREMENTS / args.total_rows)
            else:
                if args.timezone != 'local':
                    args.timezone = args.timezone.upper()
                payload = include_timestamp(payload=payload, timezone=args.timezone,
                                            enable_timezone_range=args.enable_timezone_range, performance_testing=False)

            if args.data_type != 'power' and args.table_name is not None:
                payload['table'] = args.table_name

            data.append(payload)

            if len(data) % args.batch_size == 0 or row == total_rows-1:
                publish_data.publish_data(payload=data, insert_process=args.insert_process, conns=conns,
                                          topic=args.topic, compress=args.compress, rest_timeout=args.rest_timeout,
                                          qos=args.qos, dir_name=args.dir_name, exception=args.exception)
                data = []

    else:
        while True:
            row = 0
            payload, array_counter, = row_generator(data_type=args.data_type, db_name=args.db_name,
                                                    array_counter=array_counter)
            if args.performance_testing is True:
                payload = include_timestamp(payload=payload, performance_testing=True, microseconds=MICROSECONDS,
                                            second_increments=second_increments)
                second_increments = (row + 1) * (SECOND_INCREMENTS / args.total_rows)
            else:
                if args.timezone != 'local':
                    args.timezone = args.timezone.upper()
                payload = include_timestamp(payload=payload, timezone=args.timezone,
                                            enable_timezone_range=args.enable_timezone_range, performance_testing=False)

            if args.data_type != 'power' and args.table_name is not None:
                payload['table'] = args.table_name

            data.append(payload)

            if len(data) % args.batch_size == 0:
                publish_data.publish_data(payload=data, insert_process=args.insert_process, conns=conns,
                                          topic=args.topic, compress=args.compress, rest_timeout=args.rest_timeout,
                                          qos=args.qos, dir_name=args.dir_name, exception=args.exception)
                data = []

            row += 1


if __name__ == '__main__':
    main()

