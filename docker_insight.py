import argparse
import datetime
import docker
import json
import os 
import requests
import time

from docker.errors import DockerException

TITLE_MAP = {
    "UID": "user_id",
    "PID": "process_id",
    "PPID": "parent_process_id",
    "C": "cpu_usage",
    "STIME": "start_time",
    "TTY": "terminal",
    "TIME": "cpu_time",
    "CMD": "command"
}

try:
    CLIENT = docker.from_env()
except DockerException as e:
    raise DockerException(f"❌ Docker client failed to connect: (Error; {e})")

def get_readable_io(io_stats):
    io_dict = {}
    for entry in io_stats:
        op = entry.get("op")
        value = entry.get("value")
        if op and value is not None:
            io_dict[op.lower()] = value
    return io_dict


def get_data():
    container_datas = []
    for container in CLIENT.containers.list():
        stats = container.stats(stream=False)
        top_info = container.top()
        titles = top_info['Titles']
        processes = top_info['Processes']

        created_str = container.attrs['Created']
        created_time = datetime.datetime.strptime(created_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        timestamp = datetime.datetime.utcnow()
        uptime = str(timestamp - created_time)

        for row in processes:
            blkio = get_readable_io(stats.get('blkio_stats', {}).get('io_service_bytes_recursive', []))
            net_stats = stats.get('networks', {})
            container_data = {
                'container': container.name,
                'created': created_time.isoformat(),
                'timestamp': timestamp.isoformat(),
                'uptime': uptime,
                'memory_usage_bytes': stats.get('memory_stats', {}).get('usage', 0),
                'disk_read_bytes': blkio.get('read', 0),
                'disk_write_bytes': blkio.get('write', 0),
                'network_rx_packets': sum(net.get('rx_packets', 0) for net in net_stats.values()),
                'network_tx_packets': sum(net.get('tx_packets', 0) for net in net_stats.values())
            }
            for i, title in enumerate(titles):
                container_data[TITLE_MAP[title]] = float(row[i]) if title == 'C' else row[i]
            if container_data not in container_datas:
                container_datas.append(container_data)

    return container_datas


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('conn', type=str, default=None, help='REST connection info')
    parse.add_argument('--db-name', type=str, default='new_company', help='logical database name')
    parse.add_argument('--table-name', type=str, default='docker_insight', help='logical table name')
    parse.add_argument('--wait', type=float, default=30, help='Wait time between each run')
    args = parse.parse_args()

    headers = {
        'type': 'json',
        'dbms': args.db_name,
        'table': args.table_name,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    while True:
        payload = get_data()
        try:
            response = requests.put(url=f'http://{args.conn}', headers=headers, data=json.dumps(payload))
            response.raise_for_status
        except Exception as error:
            raise Exception
        time.sleep(args.wait)

if __name__ == '__main__':
    main()



