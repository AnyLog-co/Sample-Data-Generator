# import cProfile
# import pstats
import argparse
import random
import time
import concurrent.futures

from data_generator.ping_percentagecpu import ping_sensor
from data_generator.rand_data import data_generator as rand_data
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

    def publish_payload(args, payload):
        try:
            publish_via_put(conn=args.conn, payload=payload, auth=args.auth, timeout=args.timeout, exception=args.exception)
        except Exception as e:
            if args.exception:
                print(f"Error publishing batch: {e}")

    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default='127.0.0.1:32149', help='Connection information (example: [ip]:[port])')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of rows per insert batch')
    parser.add_argument('--total-rows', type=int, default=10, help='Total rows to insert - if set to 0 then run continuously')
    parser.add_argument('--sleep', type=float, default=0.5, help='Wait time between each batch')
    parser.add_argument('--db-name', type=str, default='test', help='Logical database name')
    parser.add_argument('--auth', type=str, default=None, help='REST authentication information (ex. [user]:[password])')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--exception', action='store_true', help='Whether to print exceptions')
    parser.add_argument('--max-workers', type=int, default=10, help='number of threads to run against')
    parser.add_argument('--mode', type=str, default='streaming', choices=['file', 'streaming'], help='insert mode via REST')
    parser.add_argument('--single-insert', type=bool, const=True, nargs='?', default=False, help='Publish all data in a single insert')
    args = parser.parse_args()
    payloads = []
    if args.auth:
        args.auth = tuple(args.auth.split(":"))

    start_time = time.time()
    total_rows = 0
    print(f"Benchmark started with {args.total_rows:,} total rows | Batch Size; {args.batch_size:,}")

    try:
        while total_rows < args.total_rows:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
                # Launch multiple parallel tasks to generate the payloads
                futures = [executor.submit(generate_payload, args.db_name) for _ in range(args.batch_size)]
                # Collect the results as they complete
                payload = [future.result() for future in concurrent.futures.as_completed(futures)]

            total_rows += len(payload)
            if total_rows > args.total_rows:
               payload = payload[total_rows-args.total_rows:]
            if args.single_insert is True:
                for py in payload:
                    payloads.append(py)
            else:
                payloads.append(payload)
    except Exception as e:
        if args.exception:
            print(f"Exception occurred: {e}")

    if args.single_insert is True:
        try:
            publish_via_put(conn=args.conn, payload=payloads, auth=args.auth, timeout=args.timeout, exception=args.exception)
        except Exception as e:
            if args.exception:
                print(f"Error publishing batch: {e}")
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            # Submit tasks to the executor to run in parallel
            futures = [executor.submit(publish_payload, payload) for payload in payloads]

            # Optionally, you can wait for all futures to complete (or handle them as they finish)
            for future in concurrent.futures.as_completed(futures):
                try:
                    # You can retrieve the result here if publish_payload returned something
                    result = future.result()
                except Exception as e:
                    print(f"Exception occurred during publishing: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Benchmark completed in {elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    # profiler = cProfile.Profile()
    # profiler.enable()

    main()

    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('cumulative')
    # stats.print_stats()
