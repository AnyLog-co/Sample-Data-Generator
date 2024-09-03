import argparse
import socket
import psutil
import time
import datetime
import random
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

from declare_policies import __read_yaml

cache_lock = Lock()
cache = {
    'cpu_percent': None,
    'disk_io': None,
    'net_io': None,
    'virtual_memory': None,
    'swap_memory': None
}
CACHE_EXPIRY = 10  # seconds

def __generate_data(member_id:int=1) -> dict:
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
        'row_id': int(random.random() * 100),
        'insert_timestamp': current_time,
        'tsd_name': member_id,
        'tsd_id': int(random.random() * 1000),
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


def tcp_server(host='0.0.0.0', port=32148, member_id:int=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected by {client_address}")

                # Wait for command from client
                command = client_socket.recv(1024).decode('utf-8')

                if 'sql' in command:
                    data = __generate_data(member_id=member_id)
                    client_socket.sendall(str(data).encode('utf-8'))
                else:
                    client_socket.sendall(b'Invalid Command')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file', type=str, default='$HOME/Sample-Data-Generator/dummy_operators/dummy_configs.yaml', help='YAML operaator(s) config file')
    args = parser.parse_args()

    setup_info = __read_yaml(args.yaml_file)
    for cluster in setup_info:
        for operator in setup_info[cluster]:
            member_id = random.randmo()
            if 'member' in setup_info[cluster][operator]:
                member_id = setup_info[cluster][operator]['member']
            port = int(setup_info[cluster][operator]['port'])
            tcp_server(host='0.0.0.0', port=port, member_id=member_id)

    # Using ThreadPoolExecutor to run tasks in parallel
    # with ThreadPoolExecutor() as executor:
    #     futures = []
    #     for cluster in setup_info:
    #         for operator in setup_info[cluster]:
    #             member_id = random.randmo()
    #             if 'member' in setup_info[cluster][operator]:
    #                 member_id = setup_info[cluster][operator]['member']
    #             port = int(setup_info[cluster][operator]['port'])
    #             futures.append(executor.submit(tcp_server, '0.0.0.0', port, member_id))
    #
    #     # Optionally wait for all futures to complete
    #     for future in futures:
    #         future.result()  # This will re-raise any exception that occurred in the thread


if __name__ == "__main__":
    main()
