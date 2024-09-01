import cProfile
import pstats
import argparse
import random
import time
import psutil
import datetime
import concurrent
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def __generate_data(db_name: str) -> dict:
        uptime = int(time.time() - psutil.boot_time())
        days, remainder = divmod(uptime, 24 * 3600)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_formatted = f"{days}:{hours:02}:{minutes:02}:{seconds:02}"

        load_avg = psutil.getloadavg()
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()
        current_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        return {
            "dbms": db_name,
            "table": 'machine_info',
            'timestamp': current_time,
            'uptime': uptime_formatted,
            'node_id': random.choice(list(range(1, 11))),
            'load_avg_5min': load_avg[1],
            'disk_space': psutil.disk_usage('/').percent,
            'cpu_percent': psutil.cpu_percent(interval=1),
            'virtual_memory': psutil.virtual_memory().percent,
            'swap_memory': psutil.swap_memory().percent,
            'disk_write': disk_io.write_count,
            'disk_read': disk_io.read_count,
            'packets_recv': net_io.packets_recv,
            'packets_sent': net_io.packets_sent,
            'load_avg_15min': load_avg[2]
        }


def publish_batch(data_generators, conn, db_name, auth, timeout, exception, batch_size):
    payloads = [__generate_data(db_name=db_name) for _ in range(batch_size)]
    try:
        publish_via_put(conn=conn, payload=payloads, auth=auth, timeout=timeout, exception=exception)
    except Exception as e:
        if exception:
            print(f"Error publishing batch: {e}")



def main():
    parser = argparse.ArgumentParser()
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

    start_time = time.time()
    total_rows = 0


    batch_size = int(args.total_rows / args.batch_size) + 1
    if args.total_rows % args.batch_size == 0:
        batch_size = int(args.total_rows / args.batch_size)

    print(f"Benchmark started with {'{:,}'.format(args.total_rows)} total rows | Batch Size: {'{:,}'.format(args.batch_size)}")
    for i in range(batch_size):
        if i == 0:
            profiler = cProfile.Profile()
            profiler.enable()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(__generate_data, args.db_name) for _ in range(args.batch_size)]
            payload = [future.result() for future in concurrent.futures.as_completed(futures)]
            if i == 0:
                profiler.disable()
                stats = pstats.Stats(profiler).sort_stats('cumulative')
                stats.print_stats()
                break

        if total_rows + len(payload) > args.total_rows:
            payloads.append(payload[total_rows + len(payload) - args.total_rows:])
            total_rows = args.total_rows
        else:
            payloads.append(payload)
            total_rows += len(payload)


    # try:
    #     while total_rows < args.total_rows:
    #         payload = [__generate_data(db_name=args.db_name) for _ in range(args.batch_size)]
    #         total_rows += len(payload)
    #         if total_rows > args.total_rows:
    #            payload = payload[total_rows-args.total_rows:]
    #         if args.single_insert is True:
    #             for py in payload:
    #                 payloads.append(py)
    #         else:
    #             payloads.append(payload)
    # except Exception as e:
    #     if args.exception:
    #         print(f"Exception occurred: {e}")
    #
    # if args.single_insert is True:
    #     try:
    #         publish_via_put(conn=args.conn, payload=payloads, auth=args.auth, timeout=args.timeout, exception=args.exception)
    #     except Exception as e:
    #         if args.exception:
    #             print(f"Error publishing batch: {e}")
    # else:
    #     for payload in payloads:
    #         try:
    #             publish_via_put(conn=args.conn, payload=payload, auth=args.auth, timeout=args.timeout, exception=args.exception)
    #         except Exception as e:
    #             if args.exception:
    #                 print(f"Error publishing batch: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Benchmark completed in {elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    main()
