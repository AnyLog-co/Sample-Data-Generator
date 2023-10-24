import argparse
import json
import random

import requests

DATA = [
    {"40010":-5636,"40009":-5636,"40008":-5636,"40007":-5636,"40006":-5636,"40005":-5636,"40004":-5636,"40003":-5636,"40002":-5636,"40001":-5636},
    {"40010":4644,"40009":4644,"40008":4644,"40007":4644,"40006":4644,"40005":4644,"40004":4644,"40003":4644,"40002":4644,"40001":4644},
    {"40010":14924,"40009":14924,"40008":14924,"40007":14924,"40006":14924,"40005":14924,"40004":14924,"40003":14924,"40002":14924,"40001":14924},
    {"40010":25204,"40009":25204,"40008":25204,"40007":25204,"40006":25204,"40005":25204,"40004":25204,"40003":25204,"40002":25204,"40001":25204},
    {"40010":-30052,"40009":-30052,"40008":-30052,"40007":-30052,"40006":-30052,"40005":-30052,"40004":-30052,"40003":-30052,"40002":-30052,"40001":-30052},
]


def publish_data(conn:str=None, topic:str=None, payload:str=""):
    headers = {
        'command': 'data',
        'topic': topic,
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.post(url=f'http://{conn}', headers=headers, data=payload)
    except Exception as error:
        print(f"Failed to send data into AnyLog (Error: {error})")
        exit(1)
    else:
        if int(r.status_code) != 200:
            print(f"Failed to send data into AnyLog (Network Error: {r.status_code})")
            exit(1)


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('conn', type=str, default='127.0.0.1:32149', help='connection info')
    parse.add_argument('--topic', type=str, default='modbus', help='topic name')
    parse.add_argument('--row-count', type=int, default=1, help='number of rows to insert')
    parse.add_argument('--batch', type=int, default=1, help='number of rows per insert')
    parse.add_argument('--sleep', type=float, default=1, help='wait between each ')
    args = parse.parse_args()

    row_count = 0
    payload = []

    while row_count < args.row_count:
        payload.append(random.choice(DATA))
        row_count += 1
        if row_count == args.row_count or len(payload) == args.batch:
            str_payload = json.dumps(payload)
            publish_data(conn=args.conn, topic=args.topic, payload=str_payload)
            payload = []

if __name__ == '__main__':
    main()
