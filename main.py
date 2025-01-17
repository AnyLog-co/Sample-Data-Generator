import argparse
import asyncio
import random
import re
import time

from data_publisher.rest_server import main as rest_server
from data_publisher.opcua_server import run_opcua_server
from data_generator.configuration_based_data import describe_data, large_data, configuration_data
from data_generator.ping_percentagecpu import ping_sensor, percentagecpu_sensor
from data_generator.rand_data import data_generator as rand_data
from data_generator.blob_people_video import  get_data as people_counter
from data_generator.blobs_factory_images import get_data as image_processing


def __check_conn_info(conns:str)->str:
    """
    Check whether connection is correct format
    :args:
        conn:str - REST connection IP:Port
    :params:
        pattern:str - pattern to check connection is correct format
    :return:
        if fails then raise an error
        else - True
    """
    pattern1 = r'^(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])' \
              r'(?:\.(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])){3}:\d{1,5}$'
    pattern2 = f'^(?:[a-zA-Z0-9._%+-]+(?::[a-zA-Z0-9._%+-]+)?@)?{pattern1}'

    for conn in conns.split(","):
        if not re.match(pattern1, conn) and not re.match(pattern2, conn):
            raise argparse.ArgumentTypeError(ValueError('Connection information not in correct format - example [IP_Address]:[ANYLOG_REST_PORT]'))

    return __extract_conn(conns)


def __extract_conn(conn_info:str)->(str, tuple):
    conns = {}
    for conn in conn_info.split(","):
        auth = ()
        if '@' in conn:
            auth, conn = conn.split('@')
            auth = tuple(auth.split(':'))
        conns[conn] = auth

    return conns


def __generate_data(data_generator:str, db_name:str, last_blob:str=None, exception:bool=False):
    payload = {}
    if data_generator == 'ping':
        payload = ping_sensor(db_name=db_name)
    elif data_generator == 'percentagecpu':
        payload = percentagecpu_sensor(db_name=db_name)
    elif data_generator == 'large':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            payload = loop.run_until_complete(configuration_data())
        finally:
            loop.close()
        payload = large_data(data=payload, db_name=db_name)
    elif data_generator == 'rand':
        payload = rand_data(db_name=db_name)
    elif data_generator == 'cars':
        from data_generator.blobs_car_video import car_counting
        payload, last_blob = car_counting(db_name=db_name, last_blob=last_blob, exception=exception)
    elif data_generator == 'people':
        payload, last_blob = people_counter(db_name=db_name, last_blob=last_blob, exception=exception)
    elif data_generator == 'images':
        payload, last_blob = image_processing(db_name=db_name, last_blob=last_blob, exception=exception)

    return payload, last_blob


def __publish_data(publisher:str, conn:str, payload:list, topic:str, qos:int=0, auth:tuple=(), timeout:float=30,
                   exception:bool=False):
    if publisher == 'put':
        from data_publisher.publisher_rest import publish_via_put
        publish_via_put(conn=conn, payload=payload, auth=auth, timeout=timeout, exception=exception)
    elif publisher == 'post':
        from data_publisher.publisher_rest import publish_via_post
        publish_via_post(conn=conn, payload=payload, topic=topic, auth=auth, timeout=timeout, exception=exception)
    elif publisher == 'mqtt':
        from data_publisher.publisher_mqtt import publish_mqtt
        publish_mqtt(conn=conn, payload=payload, topic=topic, qos=qos, auth=auth, exception=exception)
    elif publisher == 'kafka':
        from data_publisher.publisher_kafka import publish_kafka
        publish_kafka(conn=conn, payload=payload, topic=topic, auth=auth, exception=exception)


def main():
    """
    positional arguments:
        data_type       data to generate
        - ping
        - percentagecpu
        - rand
        - r_50
        - large
        - car
        - people
        - factory
        publisher       format to publish data
        - put
        - post
        - mqtt
        - kafka
        - server
        - opcua
        db_name         logical database name
    :optional arguments:
        -h, --help                      show this help message and exit
        --rest-conn     REST_CONN       connection information used for PUT, POST, MQTT and Kafka (example: [user]:[passwd]@[ip]:[port])
        --batch-size    BATCH_SIZE      number of rows per insert batch
        --total-rows    TOTAL_ROWS      total rows to insert - if set to 0 then run continuously
        --sleep         SLEEP           wait time between each row to insert. For OPC-UA the sleep rate is 1/{sleep value}.
        --topic         TOPIC           topic name for POST, MQTT and Kafka
        --timeout       TIMEOUT         REST timeout
        --qos           {0,1,2,3}       Quality of Service
        --service-port  SERVICE_PORT    Server or OPC-UA service port
        --create-large-data     [CREATE_LARGE_DATA]     Create new data set for large data
        --num-tables            NUM_TABLES              when creating a large data set, number of tables
        --num-columns           NUM_COLUMNS             number of columns per
        --exception             [EXCEPTION]             Whether to print exceptions
    """
    parse = argparse.ArgumentParser()
    parse.add_argument('data_type', type=str, default='rand', help='data to generate',
                       choices=['ping', 'percentagecpu', 'rand', 'r_50', 'large', 'car', 'people', 'factory'])
    parse.add_argument('publisher', type=str, default='put', help='format to publish data',
                       choices=['put', 'post', 'mqtt', 'kafka', 'server', 'opcua'])
    parse.add_argument('db_name', type=str, default='test', help='logical database name')
    # Params used for non-server or OPC-UA
    parse.add_argument('--rest-conn', type=__check_conn_info, default='127.0.0.1:32149',
                       help='connection information used for PUT, POST, MQTT and Kafka (example: [user]:[passwd]@[ip]:[port])')
    parse.add_argument('--batch-size', type=int, default=10, help='number of rows per insert batch')
    parse.add_argument('--total-rows', type=int, default=10,
                        help='total rows to insert - if set to 0 then run continuously')
    parse.add_argument('--sleep', type=float, default=0.5,
                       help='wait time between each row to insert. For OPC-UA the sleep rate is 1/{sleep value}.')
    parse.add_argument('--topic', type=str, default='anylog-demo',
                       help='topic name for POST, MQTT and Kafka')
    parse.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parse.add_argument('--qos', type=int, choices=list(range(0, 4)), default=0,
                       help='Quality of Service')
    parse.add_argument('--service-port', type=int, default=8481, help='Server or OPC-UA service port')
    parse.add_argument('--create-large-data', type=bool, nargs='?', const=True, default=False,
                       help='Create new data set for large data')
    parse.add_argument('--num-tables', type=int, default=10,
                       help='when creating a large data set, number of tables')
    parse.add_argument('--num-columns', type=int, default=10,
                       help='number of columns per ')
    parse.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='Whether to print exceptions')
    args = parse.parse_args()

    if args.data_type in ['car', 'people', 'factory'] and args.publisher not in ['post', 'mqtt', 'kafka']:
        raise argparse.ArgumentTypeError(f"Script supports sending {args.data_type} only via POST, MQTT and Kafka.")
    if args.create_large_data is True:
        describe_data(num_tables=args.num_tables, num_columns=args.num_columns)
    if args.publisher == 'server':
        rest_server(db_name=args.db_name, service_port=args.service_port, exception=args.exception)
    elif args.publisher == 'opcua':
        asyncio.run(run_opcua_server(sleep_rate=args.sleep, db_name=args.db_name))

    payloads = []
    total_rows = 0
    last_blob = None
    while True:
        conn = random.choice(list(args.conn.keys()))
        auth = args.conn[conn]

        payload, last_blob = __generate_data(data_generator=args.data_generator, db_name=args.db_name,
                                             last_blob=last_blob, exception=args.exception)

        payloads.append(payload)
        if len(payloads) == args.batch_size or (args.total_rows <= len(payloads) + total_rows and args.total_rows != 0):
            __publish_data(publisher=args.publisher, conn=conn, payload=payloads, topic=args.topic, qos=args.qos,
                           auth=auth, timeout=args.timeout, exception=args.exception)
            total_rows += len(payloads)
            payloads = []

        if total_rows >= args.total_rows:
            exit(1)
        time.sleep(args.sleep)



if __name__ == '__main__':
    main()


