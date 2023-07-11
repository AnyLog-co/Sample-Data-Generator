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
import json

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

DATA_DIR = os.path.join(ROOT_PATH, 'data', "new-data")
MICROSECONDS = random.choice(range(100, 300000)) # initial microseconds for timestamp value
SECOND_INCREMENTS = 86400  # second increments (0.864) for 100000 rows



def __data_types(value:str)->str:
    """
    Validate data types
    :args:
        value:str - user inputted data type(s)
    :return:
        value
        if fails error
    """
    for val in value.split(","):
        if val not in ['trig', 'performance', 'ping', 'percentagecpu', 'opcua', 'power',  'examples']:
            argparse.ArgumentError(f"Unsupported data type: {val}. Supported data types: trig, performance, ping, percentagecpu, opcua, power")
    return value

def __insert_process(value:str)->str:
    """
    Validate insert process
    :args:
        value:str - user inputted process type
    :return:
        value
        if fails error
    """
    if value not in ['print', 'file', 'put', 'post', 'mqtt']:
        argparse.ArgumentError(f"Unsupported process type: {value}. Supported process types: print, file, put, post, mqtt")
    return value

class ExtendedHelpAction(argparse.Action):
    def __rows_summary(self, db_name:str='test')->str:
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
            'opcua': {"dbms": "test2", "table": "opcua_readings", "fic1_pv": -103.29249139515318,
                      "fic1_mv": -227.862187363,
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
                    print(f"\t{json.dumps(payload, indent=None)}")
            else:
                print(f"\t{json.dumps(payloads[table], indent=None)}")
        print("\n")

    def __call__(self, parser, namespace, values, option_string=None):
        # Call your function to handle extended help here
        print("Sample Data Types Aviliable")
        self.__rows_summary(db_name='test')
        setattr(namespace, self.dest, True)
        print("""Sample docker call: \ndocker run -it --detach-keys=ctrl-d --name data-generator --network host \\
                    \t-e DATA_TYPE=ping \\
                    \t-e INSERT_PROCESS=put \\
                    \t-e DB_NAME=test \\
                    \t-e TOTAL_ROWS=100 \\
                    \t-e BATCH_SIZE=10 \\
                    \t-e SLEEP=0.5 \\
                    \t-e CONN=198.74.50.131:32149,178.79.143.174:32149 \\
                    \t-e TIMEZONE=utc \\
                    \t--rm anylogco/sample-data-generator:latest\n""")



def main():
    """
    Sample data generator for AnyLog
    :positional arguments:
        data_type             type of data to insert into AnyLog.
            * trig
            * performance
            * ping
            * percentagecpu,
            * opcua, power
        insert_process        format to store generated data.
            * print
            * file
            * put
            * post
            * mqtt
        db_name               logical database name
    :optional arguments:
        -h, --help                              show this help message and exit
        --extended-help     [EXTENDED_HELP]     Generates help, but extends to include a sample row per data type
        --table-name        TABLE_NAME          Change default table name (valid for data_types except power)
        --total-rows        TOTAL_ROWS          number of rows to insert. If set to 0, will run continuously
        --batch-size        BATCH_SIZE          number of rows to insert per iteration
        --sleep             SLEEP               wait time between each row
        --timezone          TIMEZONE            timezone for generated timestamp(s)
            * local
            * utc
            * et
            * br
            * jp
            * ws
            * au
            * it
        --enable-timezone-range     [ENABLE_TIMEZONE_RANGE]     set timestamp within a range of +/- 1 month
        --performance-testing       [PERFORMANCE_TESTING]       insert all rows within a 24 hour period
        --conn      CONN            {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
        --topic     TOPIC           topic for publishing data via REST POST or MQTT
        --rest-timeout      REST_TIMEOUT        how long to wait before stopping REST
        --qos               QOS                 MQTT Quality of Service
            * 0
            * 1
            * 2
        --dir-name      DIR_NAME        directory when storing to file
        --compress      [COMPRESS]      whether to zip data dir
        --exception     [EXCEPTION]     whether to print exceptions
    :params:
        total_rows:int - row counter
        data_type_counter:int - counter used in data types
        second_increments:float - for perofmance second increments
        data:list - data to insert into AnyLog
        data_types:list - list of data types
        conns:dict - list of connections with auth information
        last_conn:list - last connection used
    :sample call:
        docker run -it --detach-keys=ctrl-d --name data-generator --network host \
            -e DATA_TYPE=ping \
            -e INSERT_PROCESS=put \
            -e DB_NAME=test \
            -e TOTAL_ROWS=100 \
            -e BATCH_SIZE=10 \
            -e SLEEP=0.5 \
            -e CONN=198.74.50.131:32149,178.79.143.174:32149 \
            -e TIMEZONE=utc \
            --rm anylogco/sample-data-generator:latest
        python3 Sample-Data-Generator/data_generator_generic.py ping put test \
            --total-rows 100 \
            --batch-size 100 \
            --sleep 0.5 \
            --conn 198.74.50.131:32149 \
            --timezone utc \
            --exception
    """
    parser = argparse.ArgumentParser(add_help=True,
        description="Sample Data Generator for AnyLog. When using a Docker based deployment, all arguments can be used as upper case environment variables.")
    parser.add_argument('data_type', type=__data_types, default='trig',
                        help='type of data to insert into AnyLog. Choices: trig, performance, ping, percentagecpu, opcua, power')
    parser.add_argument('insert_process', type=str,  default='print',
                        help='format to store generated data. Choices: print, file, put, post, mqtt')
    parser.add_argument('db_name', type=str, default='test', help='logical database name')
    parser.add_argument('--extended-help', type=bool, nargs='?', const=True, action=ExtendedHelpAction, default=False,
                        help="Generates help, but extends to include a sample row per data type")
    parser.add_argument('--table-name', type=str, default=None,
                       help='Change default table name (valid for data_types except power)')
    parser.add_argument('--total-rows', type=support.validate_row_size, default=1000000,
                       help='number of rows to insert. If set to 0, will run continuously')
    parser.add_argument('--batch-size', type=support.validate_row_size, default=10, help='number of rows to insert per iteration')
    parser.add_argument('--sleep', type=float, default=0.5, help='wait time between each row')
    parser.add_argument('--timezone', type=str, choices=['local', 'utc', 'et', 'br', 'jp', 'ws', 'au', 'it'],
                       default='local', help='timezone for generated timestamp(s)')
    parser.add_argument('--enable-timezone-range', type=bool, nargs='?', const=True, default=False,
                       help='set timestamp within a range of +/- 1 month')
    parser.add_argument('--performance-testing', type=bool, nargs='?', const=True, default=False,
                       help='insert all rows within a 24 hour period')
    parser.add_argument('--conn', type=support.validate_conn_pattern, default=None,
                       help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('--topic', type=str, default=None, help='topic for publishing data via REST POST or MQTT')
    parser.add_argument('--rest-timeout', type=float, default=30, help='how long to wait before stopping REST')
    parser.add_argument('--qos', type=int, choices=list(range(0, 3)), default=0, help='MQTT Quality of Service')
    parser.add_argument('--dir-name', type=str, default=DATA_DIR, help='directory when storing to file')
    parser.add_argument('--compress', type=bool, nargs='?', const=True, default=False, help='whether to zip data dir')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False, help='whether to print exceptions')
    args = parser.parse_args()

    args.dir_name = os.path.expanduser(os.path.expandvars(args.dir_name))

    total_rows = 0
    data_type_counter = 0
    second_increments = 0
    data = []
    if args.batch_size <= 0:
        args.batch_size = 1

    data_types = args.data_type.split(",")
    # make sure each table a unique name
    if len(data_types) > 1 and args.table_name is not None:
        args.table_name = None

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

    last_conn = None
    while True:
        data_type = random.choice(data_types)
        if data_type == 'trig':  # {"timestamp", "sin", "cos", "trig"}
            payload = trig.trig_value(db_name=args.db_name, array_counter=data_type_counter)
            data_type_counter += 1
            if data_type_counter == len(trig.VALUE_ARRAY):
                data_type_counter = 0
        elif data_type == 'performance': # {"timestamp", "value"}
            payload = performance_testing.generate_row(db_name=args.db_name, array_counter=data_type_counter)
            data_type_counter += 1
            if data_type_counter == len(performance_testing.VALUE_ARRAY):
                data_type_counter = 0
        elif data_type == 'opcua':
            payload = opcua_data.get_opcua_data(db_name=args.db_name)
        elif data_type == 'percentagecpu':
            payload = lsl_data.percentagecpu_sensor(db_name=args.db_name)
        elif data_type == 'ping':
            payload = lsl_data.ping_sensor(db_name=args.db_name)
        elif data_type == 'power':
            payload = power_company.data_generator(db_name=args.db_name)

        payload = timestamp_generator.include_timestamp(payload=payload, timezone=args.timezone,
                                                        enable_timezone_range=args.enable_timezone_range,
                                                        performance_testing=args.performance_testing,
                                                        microseconds=MICROSECONDS, second_increments=second_increments)
        if args.total_rows == 0: 
            args.performance_testing = False

        if args.performance_testing is True: 
            second_increments = (total_rows + 1) * (SECOND_INCREMENTS / args.total_rows)

        if isinstance(payload, list):
            for pyld in payload:
                data.append(pyld)
        else:
            data.append(payload)

        if len(data) % args.batch_size == 0:
            last_conn = publish_data.publish_data(payload=data, insert_process=args.insert_process, conns=conns,
                                                  topic=args.topic, compress=args.compress,
                                                  rest_timeout=args.rest_timeout, qos=args.qos, dir_name=args.dir_name,
                                                  last_conn=last_conn, exception=args.exception)
            data = []
        total_rows += 1
        if total_rows == args.total_rows:
                if len(data) != 0:
                    publish_data.publish_data(payload=data, insert_process=args.insert_process, conns=conns,
                                              topic=args.topic, compress=args.compress, rest_timeout=args.rest_timeout,
                                              qos=args.qos, dir_name=args.dir_name, last_conn=last_conn,
                                              exception=args.exception)
                exit(1)

        time.sleep(args.sleep)


if __name__ == '__main__':
    support.validate_packages()
    main()
