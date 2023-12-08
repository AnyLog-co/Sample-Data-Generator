import argparse
import os
import random
import time

from src.support.argparse_support import validate_row_size
from src.support.argparse_support import validate_sleep_time
from src.support.argparse_support import validate_conn_pattern
from src.support.argparse_support import validate_conversion_type
from src.support.argparse_support import prepare_configs

import src.data_generators.lsl_data as lsl_data
import src.data_generators.kubearmor_syslog as kubearmor_syslog
import src.data_generators.node_insight as node_insight
from src.data_generators.syslog import get_syslogs

from src.publishing_protocols.generic_protocols import print_results
from src.publishing_protocols.generic_protocols import file_results
from src.publishing_protocols.anylog_rest import AnyLogREST
from src.publishing_protocols.mqtt_protocol import AnyLogMQTT

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_PATH, 'data', "new-data")


def __generate_data(anylog_conn:AnyLogREST, db_name:str, data_type:str, batch_size:int, sleep:float, timezone:str,
                    enable_timezone_range:bool=False, exception:bool=False)->list:
    """
    Based on the data type, generate data to be stored
    """
    payloads = []
    if data_type in ['percentagecpu', 'ping']:
        payloads = lsl_data.data_generator(db_name=db_name, data_type=data_type,
                                           row_count=batch_size, timezone=timezone,
                                           timezone_range=enable_timezone_range, sleep=sleep)
    elif data_type == "kubearmor":
        payloads = kubearmor_syslog.data_generator(db_name=db_name, row_count=batch_size, sleep=sleep,
                                                   timezone=timezone, timezone_range=enable_timezone_range)
    elif data_type == "node_insight":
        payloads = node_insight.get_node_insight(anylog_conn=anylog_conn, db_name=db_name, row_count=batch_size,
                                                 sleep=sleep, timezone=timezone, exception=exception)
    elif data_type == 'syslogs':
        payloads = get_syslogs(dbname=db_name, row_count=batch_size, sleep=sleep, timezone=timezone,
                               timezone_range=enable_timezone_range, exception=exception)
    elif data_type == 'syslog':
        payloads = get_syslogs(dbname=db_name, row_count=batch_size, sleep=sleep, timezone=timezone,
                               timezone_range=enable_timezone_range, exception=exception)
    return payloads


def __publish_data(anylog_conn, insert_process:str, data_type:str, payloads:list, topic:str=None,
                   data_dir:str=None, exception:bool=False):
    if insert_process == 'print':
        print_results(payloads=payloads)
    elif insert_process == 'file':
        file_results(payloads=payloads, data_dir=data_dir, exception=exception)
    elif insert_process == 'put':
        anylog_conn.put_data(data_type=data_type, payloads=payloads)
    elif insert_process == 'post':
        anylog_conn.post_data(payloads=payloads, topic=topic)
    elif insert_process == 'mqtt':
        anylog_conn.publish_data(payloads=payloads, topic=topic)


def main():
    """
    :positional arguments:
      {ping,percentagecpu,node_insight,kubearmor,images,cars,people}
                            type of data to insert into AnyLog
      {print,file,put,post,mqtt}
                            format to store data
      db_name               logical database to store data in

    :optional arguments:
      -h, --help            show this help message and exit
      --conversion-type CONVERSION_TYPE
                            Format to convert content to be stored in AnyLog.
                            Choices: base64, bytesio, opencv
      --total-rows TOTAL_ROWS
                            total number of rows. If set to 0, then code will run
                            continuously
      --batch-size BATCH_SIZE
                            number of rows per insert
      --sleep SLEEP         wait time between each row
      --conn CONN           {user}:{password}@{ip}:{port} for sending data either
                            via REST or MQTT
      --rest-timeout REST_TIMEOUT
                            wait time before stopping REST
      --topic TOPIC         topic for publishing data via REST POST or MQTT
      --qos {0,1,2}         MQTT Quality of Service
      --dir-name DIR_NAME   directory when storing to file
      --compress [COMPRESS]
                            whether to zip data dir
      --exception [EXCEPTION]
                            whether to print exceptions
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("data_type", type=str,
                        choices=['ping', 'percentagecpu', 'node_insight', 'kubearmor', 'syslog', 'images', 'cars', 'people'],
                        default='ping', help='type of data to insert into AnyLog')
    parser.add_argument("insert_process", type=str, choices=['print', 'file', 'put', 'post', 'mqtt'], default='print',
                        help='format to store data')
    parser.add_argument('db_name', type=str, default='new_company', help='logical database to store data in')
    parser.add_argument('--conversion-type', type=validate_conversion_type, default=None,
                        help="Format to convert content to be stored in AnyLog. Choices: base64, bytesio, opencv")
    parser.add_argument('--total-rows', type=validate_row_size, default=10,
                        help='total number of rows. If set to 0, then code will run continuously')
    parser.add_argument('--batch-size', type=validate_row_size, default=10, help='number of rows per insert')
    parser.add_argument('--sleep', type=validate_sleep_time, default=0.5, help='wait time between each row')
    parser.add_argument('--conn', type=validate_conn_pattern, default=None,
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('--rest-timeout', type=validate_sleep_time, default=30, help='wait time before stopping REST')
    parser.add_argument('--topic', type=str, default=None, help='topic for publishing data via REST POST or MQTT')
    parser.add_argument('--qos', type=str, default=0, choices=list(range(0,3)), help='MQTT Quality of Service')
    parser.add_argument('--timezone', type=str, choices=['local', 'utc', 'et', 'br', 'jp', 'ws', 'au', 'it'],
                        default='local', help='timezone for generated timestamp(s)')
    parser.add_argument('--enable-timezone-range', type=bool, nargs='?', const=True, default=False,
                        help='set timestamp within a range of +/- 1 month. For performance testing, it is used to randomize the order timestamps are inserted.')
    parser.add_argument('--dir-name', type=str, default=DATA_DIR, help='directory when storing to file')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether to print exceptions')
    args = parser.parse_args()

    args.batch_size, args.conversion_type = prepare_configs(batch_size=args.batch_size, data_type=args.data_type,
                                                            conversion_type=args.conversion_type)



    if args.conn is not None and args.insert_process == 'mqtt':
        anylog_mqtt = AnyLogMQTT(conns=args.conn, qos=args.qos, exception=args.excetpion)
    elif args.conn is not None:
        anylog_conn = AnyLogREST(conns=args.conn, timeout=args.rest_timeout, exception=args.exception)
    else:
        anylog_conn = None

    row_counter = 0
    if args.total_rows == 0:
        while True:
            payloads = __generate_data(anylog_conn=anylog_conn, db_name=args.db_name, data_type=args.data_type,
                                       batch_size=args.batch_size, sleep=args.sleep, timezone=args.timezone,
                                       enable_timezone_range=args.enable_timezone_range, exception=args.exception)

            row_counter += len(payloads)
            if row_counter % args.batch_size == 0:
                __publish_data(anylog_conn=anylog_conn, insert_process=args.insert_process, data_type=args.data_type,
                               payloads=payloads, topic=args.topic, data_dir=args.dir_name, exception=args.exception)
            if args.sleep >= 0.5:
                time.sleep(args.sleep - 0.5)

    else:
        while row_counter < args.total_rows:
            payloads = __generate_data(anylog_conn=anylog_conn, db_name=args.db_name, data_type=args.data_type,
                                       batch_size=args.batch_size, sleep=args.sleep, timezone=args.timezone,
                                       enable_timezone_range=args.enable_timezone_range, exception=args.exception)

            row_counter += len(payloads)
            if row_counter % args.batch_size == 0:
                __publish_data(anylog_conn=anylog_conn, insert_process=args.insert_process, data_type=args.data_type,
                               payloads=payloads, topic=args.topic, data_dir=args.dir_name, exception=args.exception)
            if args.total_rows - row_counter < args.batch_size:
                args.batch_size = args.total_rows - row_counter

            if args.sleep >= 0.5:
                time.sleep(args.sleep - 0.5)




if __name__ == '__main__':
    main()
