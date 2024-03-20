import argparse
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

    print(output)


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
    parser.add_argument('--exception', type=bool,  nargs='?', const=True, default=False,
                        help='Whether to print exceptions')
    parser.add_argument('--examples', type=str, nargs='?', const=True, default=False, help='print example calls and sample data')
    args = parser.parse_args()

    auth, conn = __extract_conn(conn_info=args.conn)
    if args.examples:
        __generate_examples()
        exit(1)


if __name__ == '__main__':
    main()


