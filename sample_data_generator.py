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

from src.publishing_protocols.generic_protocols import print_results
from src.publishing_protocols.generic_protocols import file_results

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_PATH, 'data', "new-data")

MICROSECONDS = random.choice(range(100, 300000)) # initial microseconds for timestamp value
SECOND_INCREMENTS = 86400  # second increments (0.864) for 100000 rows



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
                        choices=['ping', 'percentagecpu', 'node_insight', 'kubearmor', 'images', 'cars', 'people'],
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
                                                            conversion_type=args.conversation_type)
    
    row_counter = 0
    while row_counter < args.total_rows:
        if args.data_type in ['percentagecpu', 'ping']:
            payloads = lsl_data.data_generator(db_name=args.db_name, data_type=args.data_type,
                                               row_count=args.batch_size, timezone=args.timezone,
                                               timezone_range=args.enable_timezone_range, sleep=args.sleep)
        elif args.data_type == "kubearmor":
            payloads = kubearmor_syslog.data_generator(db_name=args.db_name, row_count=args.batch_size, sleep=args.sleep,
                                                       timezone=args.timezone, timezone_range=args.enable_timezone_range)
        elif args.data_type == "node_insight":
            payloads = node_insight.get_node_insight(conn=conns, auth=(), timeout=args.timeout, row_count=args.batch_size,
                                                     sleep=args.sleep, timezone=args.timezone, exception=args.exception)
        row_counter += len(payloads)
        if row_counter % args.batch_size == 0:
            if args.insert_process == 'print':
                print_results(payloads=payloads)
            elif args.insert_process == 'file':
                file_results(payloads=payloads, data_dir=args.dir_name, exception=args.exception)
        if args.total_rows - row_counter < args.batch_size:
            args.batch_size = args.total_rows - row_counter

        time.sleep(args.sleep - 0.5)




if __name__ == '__main__':
    main()