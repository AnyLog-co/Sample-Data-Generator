"""
Sample MQTT client
<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=modbus and
    dbms=!default_dbms and
    table=modbus and
    column.timestamp.timestamp=now() and
    column.pt40010=(type=float and value="bring [40010]") and
    column.pt4009=(type=float and value="bring [40009]") and
    column.pt4008=(type=float and value="bring [40008]") and
    column.pt4007=(type=float and value="bring [40007]") and
    column.pt4006=(type=float and value="bring [40006]") and
    column.pt4005=(type=float and value="bring [40005]") and
    column.pt4004=(type=float and value="bring [40004]") and
    column.pt4003=(type=float and value="bring [40003]") and
    column.pt4002=(type=float and value="bring [40002]") and
    column.pt4001=(type=float and value="bring [40001]") and
)>
"""
import argparse
import json
import random

import requests

DATA = [
    {"40010":-5636,"m40009":-5636,"m40008":-5636,"m40007":-5636,"m40006":-5636,"m40005":-5636,"m40004":-5636,"m40003":-5636,"m40002":-5636,"m40001":-5636},
    {"40010":4644,"m40009":4644,"m40008":4644,"m40007":4644,"m40006":4644,"m40005":4644,"m40004":4644,"m40003":4644,"m40002":4644,"m40001":4644},
    {"40010":14924,"m40009":14924,"m40008":14924,"m40007":14924,"m40006":14924,"m40005":14924,"m40004":14924,"m40003":14924,"m40002":14924,"m40001":14924},
    {"40010":25204,"m40009":25204,"m40008":25204,"m40007":25204,"m40006":25204,"m40005":25204,"m40004":25204,"m40003":25204,"m40002":25204,"m40001":25204},
    {"40010":-30052,"m40009":-30052,"m40008":-30052,"m40007":-30052,"m40006":-30052,"m40005":-30052,"m40004":-30052,"m40003":-30052,"m40002":-30052,"m40001":-30052},
]


def put_data(conn:str=None, db_name:str="new_company", payload:str=""):
    headers = {
        'type': 'json',
        'dbms': db_name,
        'table': "modbus",
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.put(url=f'http://{conn}', headers=headers, data=payload)
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
    parse.add_argument('--row-count', type=int, default=100, help='number of rows to insert')
    parse.add_argument('--batch', type=int, default=10, help='number of rows per insert')
    parse.add_argument('--sleep', type=float, default=1, help='wait between each ')
    args = parse.parse_args()

    row_count = 0
    payload = []

    while row_count < args.row_count:
        payload.append(random.choice(DATA))
        row_count += 1
        if row_count == args.row_count or len(payload) == args.batch:
            str_payload = json.dumps(payload)
            # publish_data(conn=args.conn, topic=args.topic, payload=str_payload)
            put_data(conn=args.conn, payload=str_payload)
            payload = []

if __name__ == '__main__':
    main()
