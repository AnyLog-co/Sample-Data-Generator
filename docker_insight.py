import argparse
import datetime
import time

import docker
import json
import requests
import logging

from docker.errors import DockerException

logging.basicConfig(level=logging.INFO)

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
    raise DockerException(f"❌ Docker client failed to connect: {e}")


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
    timestamp = datetime.datetime.utcnow()

    for container in CLIENT.containers.list():
        stats = container.stats(stream=False)
        top_info = container.top()
        titles = top_info['Titles']
        processes = top_info['Processes']

        created_str = container.attrs['Created']
        created_time = datetime.datetime.strptime(created_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        uptime = str(timestamp - created_time)

        blkio = get_readable_io(stats.get('blkio_stats', {}).get('io_service_bytes_recursive', []))
        net_stats = stats.get('networks', {})

        for row in processes:
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
                mapped_key = TITLE_MAP.get(title)
                if mapped_key:
                    container_data[mapped_key] = float(row[i]) if title == 'C' else row[i]

            container_datas.append(container_data)

    return container_datas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, help='REST connection info')
    parser.add_argument('--db-name', type=str, default='new_company', help='logical database name')
    parser.add_argument('--table-name', type=str, default='docker_insight', help='logical table name')
    parser.add_argument('--wait', type=float, default=30, help='Wait time between each run')
    args = parser.parse_args()

    headers = {
        'type': 'json',
        'dbms': args.db_name,
        'table': args.table_name,
        'mode': 'streaming',
        'Content-Type': 'application/json'
    }

    while True:
        payloads = get_data()
        logging.info(f"Sending payload to {args.conn}")
        for payload in payloads:
            try:
                response = requests.put(url=f'http://{args.conn}', headers=headers, data=json.dumps(payload))
                response.raise_for_status()
                logging.info(f"✅ Payload sent successfully with status {response.status_code}")
            except Exception as error:
                logging.error(f"❌ Failed to send data: {error}")
                raise
        time.sleep(args.wait)


if __name__ == '__main__':
    main()
