import argparse
import json
import random
import time

DATA = 'flexnode_data.json'

def __extract_conn(conn_info:str)->(str, tuple):
    conns = {}
    for conn in conn_info.split(","):
        auth = ()
        if '@' in conn:
            auth, conn = conn.split('@')
            auth = tuple(auth.split(':'))
        conns[conn] = auth
    return conns

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
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='connection information (example: [user]:[passwd]@[ip]:[port])')
    parser.add_argument('publisher', type=str, default='put',
                        choices=['put', 'post', 'mqtt', 'kafka'], help='format to publish data')
    parser.add_argument('--topic', type=str, default='anylog-demo', help='topic name for POST, MQTT and Kafka')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--qos', type=int, choices=list(range(0, 4)), default=0, help='Quality of Service')
    parser.add_argument('--exception', type=bool,  nargs='?', const=True, default=False,
                        help='Whether to print exceptions')
    parser.add_argument('--examples', type=str, nargs='?', const=True, default=False, help='print example calls and sample data')
    args = parser.parse_args()

    conns = __extract_conn(conn_info=args.conn)
    conn = list(conns.keys())[0]
    auth = conns[conn]


    try:
        with open(DATA, 'r') as f:
            output = f.readlines()
    except Exception as error:
        print(f"failed to read content in {DATA} (Error: {error})")

    for line in output:
        __publish_data(publisher=args.publisher, conn=conn, payload=json.loads(line), topic=args.topic, qos=args.qos,
                       auth=auth, timeout=args.timeout, exception=args.exception)

if __name__ == '__main__':
    main()


