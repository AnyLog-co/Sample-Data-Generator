# import cProfile
# import pstats
import argparse
import random
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from data_generator.ping_percentagecpu import ping_sensor
from data_generator.rand_data import data_generator as rand_data
from data_generator.machine_insight import random_machine_data, machine_data
from data_publisher.publisher_rest import publish_via_put


BATCH_TIME = []
INSERT_TIME = []
PAYLOAD = {}

def __extract_conn(conn_info: str) -> dict:
    conns = {}
    for conn in conn_info.split(","):
        auth = ()
        if '@' in conn:
            auth, conn = conn.split('@')
            auth = tuple(auth.split(':'))
        conns[conn] = auth
    return conns


def __generate_data(data_generator: str, db_name: str) -> dict:
    if data_generator == 'ping':
        return ping_sensor(db_name=db_name)
    elif data_generator == 'rand':
        return rand_data(db_name=db_name)
    elif data_generator == 'rand_machine':
        return random_machine_data(db_name=db_name)
    elif data_generator == 'machine':
        return machine_data(db_name=db_name)
    return {}


def publish_batch(data_generators, conn, db_name, auth, timeout, exception, batch_size):
    payloads = [__generate_data(random.choice(data_generators), db_name) for _ in range(batch_size)]
    try:
        publish_via_put(conn=conn, payload=payloads, auth=auth, timeout=timeout, exception=exception)
    except Exception as e:
        if exception:
            print(f"Error publishing batch: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_generator', type=str, default='rand', choices=['rand', 'ping', 'rand_machine', 'machine'], help='Data to generate')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149', help='Connection information (example: [ip]:[port])')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of rows per insert batch')
    parser.add_argument('--total-rows', type=int, default=10, help='Total rows to insert - if set to 0 then run continuously')
    parser.add_argument('--sleep', type=float, default=0.5, help='Wait time between each batch')
    parser.add_argument('--db-name', type=str, default='test', help='Logical database name')
    parser.add_argument('--auth', type=str, default=None, help='REST authentication information (ex. [user]:[password])')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--exception', action='store_true', help='Whether to print exceptions')
    parser.add_argument('--max-workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--single-insert', type=bool, const=True, nargs='?', default=False, help='Publish all data in a single insert')
    args = parser.parse_args()
    payloads = []
    if args.auth:
        args.auth = tuple(args.auth.split(":"))
    data_generators = args.data_generator.split(",")

    start_time = time.time()
    total_rows = 0
    print(f"Benchmark started with {args.total_rows:,} total rows | Batch Size: {args.batch_size:,} | Data Generator: {data_generators}")

    try:
        while total_rows < args.total_rows:
            batch_start_time = time.time()
            payload = [__generate_data(random.choice(data_generators), args.db_name) for _ in range(args.batch_size)]
            BATCH_TIME.append(time.time() - batch_start_time)
            if PAYLOAD == {}:
                PAYLOAD['sample'] = json.dumps(payload[0])
                PAYLOAD['size'] = len(PAYLOAD['sample'])
            total_rows += len(payload)
            if total_rows > args.total_rows:
               payload = payload[total_rows-args.total_rows:]
            if args.single_insert is True:
                for py in payload:
                    payloads.append(py)
            else:
                payloads.append(payload)
            print(f'\t- Batch Number: {total_rows/args.batch_size} | Batch Processing Time: {BATCH_TIME[-1]:.2} seconds')
    except Exception as e:
        if args.exception:
            print(f"Exception occurred: {e}")

    if args.single_insert is True:
        start_insert = time.time()
        try:
            publish_via_put(conn=args.conn, payload=payloads, auth=args.auth, timeout=args.timeout, exception=args.exception)
        except Exception as e:
            if args.exception:
                print(f"Error publishing batch: {e}")
        INSERT_TIME.append(time.time() - start_insert)
    else:
        for payload in payloads:
            start_insert = time.time()
            try:
                publish_via_put(conn=args.conn, payload=payload, auth=args.auth, timeout=args.timeout,
                                exception=args.exception)
            except Exception as e:
                if args.exception:
                    print(f"Error publishing batch: {e}")
            INSERT_TIME.append(time.time() - start_insert)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"""----------------------------------------------------------------
Benchmark completed in {elapsed_time:.2f} seconds.
\tTotal Batch Time: {sum(BATCH_TIME):.2f} seconds | AVG: {sum(BATCH_TIME)/len(BATCH_TIME):.2f} seconds | MIN: {min(BATCH_TIME):.2f} seconds | Max: {max(BATCH_TIME):.2f} seconds 
\tTotal Insert Time: {sum(INSERT_TIME):.2f} seconds | AVG: {sum(INSERT_TIME)/len(INSERT_TIME):.2f} seconds | MIN: {min(INSERT_TIME):.2f} seconds | Max: {max(INSERT_TIME):.2f} seconds
\tSample Data: {PAYLOAD['sample']} | Data Size: {PAYLOAD['size']} 
----------------------------------------------------------------""")

if __name__ == '__main__':
    # profiler = cProfile.Profile()
    # profiler.enable()

    main()

    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('cumulative')
    # stats.print_stats()
