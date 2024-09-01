# import cProfile
# import pstats
import argparse
import random
import time
import concurrent.futures

from data_publisher.publisher_rest import publish_via_put
import psutil
import datetime
from threading import Lock

cache_lock = Lock()
cache = {
    'cpu_percent': None,
    'disk_io': None,
    'net_io': None,
    'virtual_memory': None,
    'swap_memory': None
}
CACHE_EXPIRY = 10  # seconds


def __extract_conn(conn_info: str) -> dict:
    conns = {}
    for conn in conn_info.split(","):
        auth = ()
        if '@' in conn:
            auth, conn = conn.split('@')
            auth = tuple(auth.split(':'))
        conns[conn] = auth
    return conns

def __generate_data(db_name: str) -> dict:
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Cache results
    with cache_lock:
        cache_time = time.time()
        if cache['cpu_percent'] is None or (cache_time - cache.get('timestamp', 0) > CACHE_EXPIRY):
            cache['cpu_percent'] = psutil.cpu_percent(interval=1)
            cache['disk_io'] = psutil.disk_io_counters()
            cache['net_io'] = psutil.net_io_counters()
            cache['virtual_memory'] = psutil.virtual_memory().percent
            cache['swap_memory'] = psutil.swap_memory().percent
            cache['timestamp'] = cache_time

    uptime = int(time.time() - psutil.boot_time())
    days, remainder = divmod(uptime, 24 * 3600)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_formatted = f"{days}:{hours:02}:{minutes:02}:{seconds:02}"

    load_avg = psutil.getloadavg()
    disk_io = cache['disk_io']
    net_io = cache['net_io']

    return {
        "dbms": db_name,
        "table": 'machine_info',
        'timestamp': current_time,
        'uptime': uptime_formatted,
        'node_id': random.choice(range(1, 11)),
        'load_avg_5min': load_avg[1],
        'disk_space': psutil.disk_usage('/').percent,
        'cpu_percent': cache['cpu_percent'],
        'virtual_memory': cache['virtual_memory'],
        'swap_memory': cache['swap_memory'],
        'disk_write': disk_io.write_count,
        'disk_read': disk_io.read_count,
        'packets_recv': net_io.packets_recv,
        'packets_sent': net_io.packets_sent,
        'load_avg_15min': load_avg[2]
    }
def __generate_data(db_name: str) -> dict:
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Cache results
    with cache_lock:
        cache_time = time.time()
        if cache['cpu_percent'] is None or (cache_time - cache.get('timestamp', 0) > CACHE_EXPIRY):
            cache['cpu_percent'] = psutil.cpu_percent(interval=1)
            cache['disk_io'] = psutil.disk_io_counters()
            cache['net_io'] = psutil.net_io_counters()
            cache['virtual_memory'] = psutil.virtual_memory().percent
            cache['swap_memory'] = psutil.swap_memory().percent
            cache['timestamp'] = cache_time

    uptime = int(time.time() - psutil.boot_time())
    days, remainder = divmod(uptime, 24 * 3600)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_formatted = f"{days}:{hours:02}:{minutes:02}:{seconds:02}"

    load_avg = psutil.getloadavg()
    disk_io = cache['disk_io']
    net_io = cache['net_io']

    return {
        "dbms": db_name,
        "table": 'machine_info',
        'timestamp': current_time,
        'uptime': uptime_formatted,
        'node_id': random.choice(range(1, 11)),
        'load_avg_5min': load_avg[1],
        'disk_space': psutil.disk_usage('/').percent,
        'cpu_percent': cache['cpu_percent'],
        'virtual_memory': cache['virtual_memory'],
        'swap_memory': cache['swap_memory'],
        'disk_write': disk_io.write_count,
        'disk_read': disk_io.read_count,
        'packets_recv': net_io.packets_recv,
        'packets_sent': net_io.packets_sent,
        'load_avg_15min': load_avg[2]
    }


def publish_batch(data_generators, conn, db_name, auth, timeout, exception, batch_size):
    payloads = [__generate_data(db_name) for _ in range(batch_size)]
    try:
        publish_via_put(conn=conn, payload=payloads, auth=auth, timeout=timeout, exception=exception)
    except Exception as e:
        if exception:
            print(f"Error publishing batch: {e}")


def main():
    def generate_payload(db_name):
        return __generate_data(db_name)

    def publish_payload(conn, payload, auth, timeout, exception):
        try:
            publish_via_put(conn=conn, payload=payload, auth=auth, timeout=timeout, exception=exception)
        except Exception as e:
            if exception:
                print(f"Error publishing batch: {e}")

    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='Connection information (example: [ip]:[port])')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of rows per insert batch')
    parser.add_argument('--total-rows', type=int, default=10,
                        help='Total rows to insert - if set to 0 then run continuously')
    parser.add_argument('--sleep', type=float, default=0.5, help='Wait time between each batch')
    parser.add_argument('--db-name', type=str, default='test', help='Logical database name')
    parser.add_argument('--auth', type=str, default=None,
                        help='REST authentication information (ex. [user]:[password])')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--exception', action='store_true', help='Whether to print exceptions')
    parser.add_argument('--max-workers', type=int, default=10, help='number of threads to run against')
    parser.add_argument('--mode', type=str, default='streaming', choices=['file', 'streaming'],
                        help='insert mode via REST')
    parser.add_argument('--single-insert', type=bool, const=True, nargs='?', default=False,
                        help='Publish all data in a single insert')
    args = parser.parse_args()

    if args.auth:
        args.auth = tuple(args.auth.split(":"))

    total_rows = 0
    payloads = []
    print(f"Benchmark started with {args.total_rows:,} total rows | Batch Size: {args.batch_size:,}")

    try:
        while total_rows < args.total_rows:
            # Generate batch of data
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
                futures = [executor.submit(generate_payload, args.db_name) for _ in range(args.batch_size)]
                payload = [future.result() for future in concurrent.futures.as_completed(futures)]

            total_rows += len(payload)
            if total_rows > args.total_rows:
                payload = payload[:args.total_rows - total_rows + len(payload)]

            if args.single_insert:
                payloads.extend(payload)
            else:
                # Publish immediately when batch size is reached
                publish_payload(args.conn, payload, args.auth, args.timeout, args.exception)

            if not args.single_insert:
                time.sleep(args.sleep)

    except Exception as e:
        if args.exception:
            print(f"Exception occurred: {e}")

    if args.single_insert and payloads:
        # Publish all data at once if single_insert is True
        publish_payload(args.conn, payloads, args.auth, args.timeout, args.exception)

    print(f"Benchmark completed with {total_rows:,} rows inserted.")


def main():
    def generate_payload(db_name):
        return __generate_data(db_name)

    def publish_payload(conn, payload, auth, timeout, exception):
        try:
            publish_via_put(conn=conn, payload=payload, auth=auth, timeout=timeout, exception=exception)
        except Exception as e:
            if exception:
                print(f"Error publishing batch: {e}")

    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='Connection information (example: [ip]:[port])')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of rows per insert batch')
    parser.add_argument('--total-rows', type=int, default=10,
                        help='Total rows to insert - if set to 0 then run continuously')
    parser.add_argument('--sleep', type=float, default=0.5, help='Wait time between each batch')
    parser.add_argument('--db-name', type=str, default='test', help='Logical database name')
    parser.add_argument('--auth', type=str, default=None,
                        help='REST authentication information (ex. [user]:[password])')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--exception', action='store_true', help='Whether to print exceptions')
    parser.add_argument('--max-workers', type=int, default=10, help='number of threads to run against')
    parser.add_argument('--mode', type=str, default='streaming', choices=['file', 'streaming'],
                        help='insert mode via REST')
    parser.add_argument('--single-insert', type=bool, const=True, nargs='?', default=False,
                        help='Publish all data in a single insert')
    args = parser.parse_args()

    if args.auth:
        args.auth = tuple(args.auth.split(":"))

    total_rows = 0
    payloads = []
    print(f"Benchmark started with {args.total_rows:,} total rows | Batch Size: {args.batch_size:,}")

    try:
        while total_rows < args.total_rows:
            # Generate batch of data
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
                futures = [executor.submit(generate_payload, args.db_name) for _ in range(args.batch_size)]
                payload = [future.result() for future in concurrent.futures.as_completed(futures)]

            total_rows += len(payload)
            if total_rows > args.total_rows:
                payload = payload[:args.total_rows - total_rows + len(payload)]

            if args.single_insert:
                payloads.extend(payload)
            else:
                # Publish immediately when batch size is reached
                publish_payload(args.conn, payload, args.auth, args.timeout, args.exception)

            if not args.single_insert:
                time.sleep(args.sleep)

    except Exception as e:
        if args.exception:
            print(f"Exception occurred: {e}")

    if args.single_insert and payloads:
        # Publish all data at once if single_insert is True
        publish_payload(args.conn, payloads, args.auth, args.timeout, args.exception)

    print(f"Benchmark completed with {total_rows:,} rows inserted.")


if __name__ == '__main__':
    # profiler = cProfile.Profile()
    # profiler.enable()

    main()

    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('cumulative')
    # stats.print_stats()
