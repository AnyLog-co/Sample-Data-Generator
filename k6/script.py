import argparse
import requests
import orjson
import time
import datetime
import psutil
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

TABLE_NAME = 'python3_performance'

def publish_via_put(conn: str, payload: list, auth: tuple = (), timeout: float = 30, exception: bool = False):
    headers = {
        'type': 'json',
        'dbms': payload[0]['dbms'] if isinstance(payload, list) else payload['dbms'],
        'table': payload[0]['table'] if isinstance(payload, list) else payload['table'],
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    if isinstance(payload, list):
        for row in payload:
            del row['dbms']
            del row['table']
    elif isinstance(payload, dict):
        del payload['dbms']
        del payload['table']

    start_request = time.time()
    try:
        r = requests.put(f'http://{conn}', headers=headers, data=orjson.dumps(payload), auth=auth, timeout=timeout)
        response_time = time.time() - start_request
    except Exception as error:
        response_time = timeout
        if exception:
            print(f"Failed to execute PUT against {conn} (Error: {error})")
        return False, response_time

    success = r.status_code // 100 == 2
    if not success and exception:
        print(f"Failed to execute PUT against {conn} (Network Error: {r.status_code})")
    return success, response_time

def generate_single_row(nodeID: int, db_name: str, table_name: str):
    uptime = int(time.time() - psutil.boot_time())
    days = uptime // (24 * 3600)
    hours = (uptime % (24 * 3600)) // 3600
    minutes = (uptime % 3600) // 60
    seconds = uptime % 60
    uptime_formatted = f"{days}:{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"

    load_avg = psutil.getloadavg()
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()

    return {
        "dbms": db_name,
        "table": table_name,
        'timestamp': datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'uptime': uptime_formatted,
        'node_id': nodeID + 1,
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
    parser.add_argument('--single-insert', action='store_true', help='Publish all data in a single insert')
    args = parser.parse_args()

    if args.auth:
        args.auth = tuple(args.auth.split(':'))

    metrics = defaultdict(list)
    payloads = []
    start_time = time.time()
    total_rows = 0
    print(f"Benchmark started with {args.total_rows} total rows...")

    try:
        with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            while total_rows < args.total_rows:
                futures = [executor.submit(generate_single_row, nodeID=i, db_name=args.db_name, table_name=TABLE_NAME)
                           for i in range(args.batch_size)]

                for future in as_completed(futures):
                    payloads.append(future.result())
                    total_rows += 1
                    if total_rows >= args.total_rows:
                        break
    except Exception as e:
        if args.exception:
            print(f"Exception occurred: {e}")

    if args.single_insert:
        try:
            status, response_time = publish_via_put(conn=args.conn, payload=payloads, auth=args.auth,
                                                    timeout=args.timeout, exception=args.exception)
            metrics['response_times'].append(response_time)
            if not status:
                metrics['errors'].append(1)
        except Exception as e:
            if args.exception:
                print(f"Error publishing batch: {e}")
            metrics['errors'].append(1)
    else:
        payload_batches = [payloads[i:i + args.batch_size] for i in range(0, len(payloads), args.batch_size)]
        with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            futures = [executor.submit(publish_via_put, conn=args.conn, payload=batch, auth=args.auth,
                                       timeout=args.timeout, exception=args.exception) for batch in payload_batches]
            for future in as_completed(futures):
                status, response_time = future.result()
                metrics['response_times'].append(response_time)
                if not status:
                    metrics['errors'].append(1)

    end_time = time.time()
    elapsed_time = end_time - start_time

    total_requests = len(metrics['response_times'])
    total_errors = len(metrics['errors'])
    avg_response_time = sum(metrics['response_times']) / total_requests if total_requests > 0 else 0
    rps = total_requests / elapsed_time if elapsed_time > 0 else 0

    print(f"Benchmark completed in {elapsed_time:.2f} seconds.")
    print(f"Requests per second (RPS): {rps:.2f}")
    print(f"Average response time: {avg_response_time:.2f} seconds")
    print(f"Total requests: {total_requests}")
    print(f"Total errors: {total_errors}")

if __name__ == '__main__':
    main()
