import argparse
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from data_generator.ping_percentagecpu import ping_sensor
from data_generator.rand_data import data_generator as rand_data
from data_publisher.publisher_rest import publish_via_put


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
    payload = {}
    if data_generator == 'ping':
        payload = ping_sensor(db_name=db_name)
    elif data_generator == 'rand':
        payload = rand_data(db_name=db_name)
    return payload


def publish_batch(data_generators, conn, db_name, auth, timeout, exception, batch_size):
    payloads = []
    for _ in range(batch_size):
        data_generator = random.choice(data_generators)
        payload = __generate_data(data_generator=data_generator, db_name=db_name)
        payloads.append(payload)

    publish_via_put(conn=conn, payload=payloads, auth=auth, timeout=timeout, exception=exception)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_generator', type=str, default='rand', choices=['rand', 'ping'], help='data to generate')
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='connection information (example: [ip]:[port])')
    parser.add_argument('--batch-size', type=int, default=10, help='number of rows per insert batch')
    parser.add_argument('--total-rows', type=int, default=10,
                        help='total rows to insert - if set to 0 then run continuously')
    parser.add_argument('--sleep', type=float, default=0.5, help='wait time between each row to insert')
    parser.add_argument('--db-name', type=str, default='test', help='logical database name')
    parser.add_argument('--auth', type=str, default=None,
                        help='REST authentication information (ex. [user]:[password])')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--exception', action='store_true', help='Whether to print exceptions')
    parser.add_argument('--max-workers', type=int, default=4, help='number of parallel workers')
    args = parser.parse_args()

    if args.auth:
        args.auth = tuple(args.auth.split(":"))
    data_generators = args.data_generator.split(",")

    start_time = time.time()
    total_rows = 0
    print(f"Benchmark started with {args.total_rows} total rows...")

    try:
        with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            futures = []
            while args.total_rows == 0 or total_rows < args.total_rows:
                futures.append(
                    executor.submit(publish_batch, data_generators, args.conn, args.db_name, args.auth, args.timeout,
                                    args.exception, args.batch_size))
                total_rows += args.batch_size
                if args.total_rows > 0 and total_rows >= args.total_rows:
                    break
                time.sleep(args.sleep)

            for future in as_completed(futures):
                future.result()  # This will re-raise any exceptions that occurred in the thread
    except Exception as e:
        if args.exception:
            print(f"Exception occurred: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Benchmark completed in {elapsed_time:.2f} seconds.")


if __name__ == '__main__':
    main()
