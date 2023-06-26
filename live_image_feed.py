import argparse
import importlib
import os
import sys
import time

for package in ['cv2', 'numpy']:
    if not importlib.util.find_spec(package):
        raise ImportError(f"Failed to locate {package} package")

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_PATH, 'data')
DATA_GENERATORS = os.path.join(ROOT_PATH, 'data_generators')
PUBLISHING_PROTOCOLS = os.path.join(ROOT_PATH, 'publishing_protocols')
sys.path.insert(0, DATA_GENERATORS)
sys.path.insert(0, PUBLISHING_PROTOCOLS)

import publishing_protocols.support as support
import publishing_protocols.publish_data as publish_data
import data_generators.live_feed as live_feed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('insert_process', type=str, choices=['print', 'file', 'put', 'post', 'mqtt'],
                        default='print', help='format to store generated data')
    parser.add_argument('--db-name', type=str, default='test', help='logical database name')
    parser.add_argument('--table-name', type=str, default=None,
                        help='Change default table name (valid for data_types except power)')
    parser.add_argument('--total-rows', type=support.validate_row_size, default=1000000,
                        help='number of rows to insert. If set to 0, will run continuously')
    parser.add_argument('--batch-size', type=support.validate_row_size, default=10,
                        help='number of rows to insert per iteration')
    parser.add_argument('--sleep', type=float, default=0.5, help='wait time between each row')
    parser.add_argument('--camera-port', type=int, default=0, help='Port to get images from')
    parser.add_argument('--conns', type=support.validate_conn_pattern, default=None,
                        help='{user}:{password}@{ip}:{port} for sending data either via REST or MQTT')
    parser.add_argument('--topic', type=str, default=None, help='topic for publishing data via REST POST or MQTT')
    parser.add_argument('--rest-timeout', type=float, default=30, help='how long to wait before stopping REST')
    parser.add_argument('--qos', type=int, choices=list(range(0, 3)), default=0, help='MQTT Quality of Service')
    parser.add_argument('--dir-name', type=str, default=DATA_DIR, help='directory when storing to file')
    parser.add_argument('--compress', type=bool, nargs='?', const=True, default=False, help='whether to zip data dir')
    parser.add_argument('--list-ports', type=bool, nargs='?', const=True, default=False, help='print list of open ports')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether to print exceptions')
    args = parser.parse_args()

    if args.list_ports is True:
        print(live_feed.list_ports())
        exit(1)
    total_rows = 0
    data = []
    while True:
        payload = live_feed.generate_reading(db_name=args.db_name, table_name=args.table_name, camera_id=args.camera_port)
        data.append(payload)
        if len(data) % args.batch_size == 0:
            publish_data.publish_data(payload=data, insert_process=args.protocol, conns=args.conns, topic=args.topic,
                                      qos=args.qos, rest_timeout=args.timeout, dir_name=args.results_dir, compress=args.compress,
                                      exception=args.exception)
            data = []
        total_rows += 1
        if total_rows == args.total_rows:
            if len(data) > 0:
                publish_data.publish_data(payload=data, insert_process=args.protocol, conns=args.conns,
                                          topic=args.topic,
                                          qos=args.qos, rest_timeout=args.timeout, dir_name=args.results_dir,
                                          compress=args.compress,
                                          exception=args.exception)
            exit(1)

        time.sleep(args.sleep)


if __name__ == '__main__':
    main()
