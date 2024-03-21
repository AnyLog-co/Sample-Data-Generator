import argparse
import time

from data_generator import ping_percentagecpu, rand_data
from data_generator.support import serialize_data


def __extract_conn(conn_info:str)->(str, tuple):
    auth = ()
    conn = conn_info
    if '@' in conn_info:
        auth, conn = conn_info.split('@')
        auth = tuple(auth.split(':'))
    return auth, conn

def __generate_examples():
    output = "Sample Values:"
    output += f"\n\t{serialize_data(rand_data.data_generator(db_name='test'))}"
    output += f"\n\t{serialize_data(ping_percentagecpu.ping_sensor(db_name='test'))}"
    output += f"\n\t{serialize_data(ping_percentagecpu.percentagecpu_sensor(db_name='test'))}"
    output += "\n\nSample Calls"
    output += "\n\tSending data to MQTT: python3 ~/Sample-Data-Generator/data_generator.py rand localhost:1883 mqtt --topic test --exception"
    output += "\n\tSending data to Kafka: python3 ~/Sample-Data-Generator/data_generator.py rand 35.188.2.231:9092 kafka --topic test --exception"
    output += "\n\tSending data via REST POST: python3 ~/Sample-Data-Generator/data_generator.py rand 127.0.0.1:32149 post --topic test --exception"
    output += "\n\tSending data via REST PUT: python3 ~/Sample-Data-Generator/data_generator.py rand 127.0.0.1:32149 put --exception"
    print(output)


def __generate_data(data_generator:str, db_name:str)->dict:
    if data_generator == 'ping':
        return ping_percentagecpu.ping_sensor(db_name=db_name)
    elif data_generator == 'percentagecpu':
        return ping_percentagecpu.percentagecpu_sensor(db_name=db_name)
    elif data_generator == 'rand':
        return rand_data.data_generator(db_name=db_name)


def __publish_data(publisher:str, conn:str, payload:list, topic:str, qos:int=0, auth:tuple=(), timeout:float=30, exception:bool=False):
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
    parser = argparse.ArgumentParser()
    parser.add_argument('data_generator', type=str, default='rand',
                        choices=['rand', 'ping', 'percentagecpu'], help='data to generate')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='connection information (example: [user]:[passwd]@[ip]:[port]')
    parser.add_argument('publisher', type=str, default='put',
                        choices=['put', 'post', 'mqtt', 'kafka'], help='format to publish data')
    parser.add_argument('--batch-size', type=int, default=10, help='number of rows per insert batch')
    parser.add_argument('--total-rows', type=int, default=10, help='total rows to insert - if set to 0 then run continuously')
    parser.add_argument('--sleep', type=float, default=0.5, help='wait time between each row to insert')
    parser.add_argument('--db-name', type=str, default='test', help='logical database name')
    parser.add_argument('--topic', type=str, default='anylog-demo', help='topic name for POST, MQTT and Kafka')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--qos', type=int, choices=list(range(0, 4)), default=0, help='Quality of Service')
    parser.add_argument('--exception', type=bool,  nargs='?', const=True, default=False,
                        help='Whether to print exceptions')
    parser.add_argument('--examples', type=str, nargs='?', const=True, default=False, help='print example calls and sample data')
    args = parser.parse_args()

    auth, conn = __extract_conn(conn_info=args.conn)
    total_rows = 0
    payloads = []

    if args.examples:
        __generate_examples()
        exit(1)


    while True:
        payloads.append(__generate_data(data_generator=args.data_generator, db_name=args.db_name))
        if len(payloads) == args.batch_size or total_rows + len(payloads) >= args.total_rows:
            __publish_data(publisher=args.publisher, conn=conn, payload=payloads, topic=args.topic, qos=args.qos,
                           auth=auth, timeout=args.timeout, exception=args.exception)
            total_rows += len(payloads)
        if total_rows >= args.total_rows:
            exit(1)
        time.sleep(args.sleep)




if __name__ == '__main__':
    main()


