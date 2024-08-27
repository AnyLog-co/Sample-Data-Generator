import argparse
import requests
import orjson
import random
import time
from datetime import datetime
import psutil
from collections import defaultdict

TABLE_NAME = 'python3_performance'


def publish_via_put(conn: str, payload: list, auth: tuple = (), timeout: float = 30, exception: bool = False):
    status = True
    headers = {
        'type': 'json',
        'dbms': None,
        'table': None,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    if isinstance(payload, list):
        headers['dbms'] = payload[0]['dbms']
        headers['table'] = payload[0]['table']
        for row in payload:
            del row['dbms']
            del row['table']
    elif isinstance(payload, dict):
        headers['dbms'] = payload['dbms']
        headers['table'] = payload['table']
        del payload['dbms']
        del payload['table']

    start_request = time.time()
    try:
        r = requests.put(url=f'http://{conn}', headers=headers, data=orjson.dumps(payload), auth=auth, timeout=timeout)
        response_time = time.time() - start_request
    except Exception as error:
        status = False
        response_time = timeout
        if exception is True:
            print(f"Failed to execute PUT against {conn} (Error: {error})")
    else:
        status = str(r.status_code).startswith('2')
        if status is False and exception is True:
            print(f"Failed to execute PUT against {conn} (Network Error: {r.status_code})")
    return status, response_time


def generate_single_row(nodeID: int, db_name: str, table_name: str):
    def __uptime() -> str:
        # Get the uptime of the system in seconds
        uptime = int(time.time() - psutil.boot_time())

        # Convert uptime to days, hours, minutes, and seconds
        days = uptime // (24 * 3600)
        hours = (uptime % (24 * 3600)) // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60

        # Format uptime as D:HH:MM:SS
        uptime_formatted = f"{days}:{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
        return uptime_formatted

    # Get real system metrics using psutil
    load_avg = psutil.getloadavg()  # (1min, 5min, 15min) load averages
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()

    return {
        'timestamp': datetime.utcnow().isoformat(),
        'uptime': __uptime(),
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
    parser.add_argument('data_generator', type=str, default='rand', choices=['rand', 'ping'], help='Data to generate')
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
    parser.add_argument('--max-workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--single-insert', type=bool, const=True, nargs='?', default=False,
                        help='Publish all data in a single insert')
    args = parser.parse_args()

    # Metrics storage
    metrics = defaultdict(list)

    payloads = []
    start_time = time.time()
    total_rows = 0
    print(f"Benchmark started with {args.total_rows} total rows...")

    try:
        while total_rows < args.total_rows:
            payload = [generate_single_row(nodeID=i, db_name=args.db_name, table_name=TABLE_NAME) for i in
                       range(args.batch_size)]
            total_rows += len(payload)
            if total_rows > args.total_rows:
                payload = payload[total_rows - args.total_rows:]
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
        for payload in payloads:
            try:
                status, response_time = publish_via_put(conn=args.conn, payload=payload, auth=args.auth,
                                                        timeout=args.timeout, exception=args.exception)
                metrics['response_times'].append(response_time)
                if not status:
                    metrics['errors'].append(1)
            except Exception as e:
                if args.exception:
                    print(f"Error publishing batch: {e}")
                metrics['errors'].append(1)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Performance metrics calculation
    total_requests = len(metrics['response_times'])
    total_errors = len(metrics['errors'])
    avg_response_time = sum(metrics['response_times']) / total_requests
    rps = total_requests / elapsed_time

    print(f"Benchmark completed in {elapsed_time:.2f} seconds.")
    print(f"Requests per second (RPS): {rps:.2f}")
    print(f"Average response time: {avg_response_time:.2f} seconds")
    print(f"Total requests: {total_requests}")
    print(f"Total errors: {total_errors}")


if __name__ == '__main__':
    main()
