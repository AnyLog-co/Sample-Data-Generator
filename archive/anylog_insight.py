import argparse
import datetime
import ast
import json
import random
import requests
import time

COMMANDS = {
    'network_io': 'get node info net_io_counters',
    'disk_io': 'get node info disk_io_counters',
}

def __get_command(conn:str, query:str)->str:
    """
    Execute GET command
    :args:
        conn:str - REST connection information
        query:str - query to execute
    :params:
        headers:dict - REST header information
        r:requests.GET - results from rest request
    :return:
        results from REST request
    """
    header = {
        'command': query,
        'User-Agent': 'AnyLog/1.23'
    }
    try:
        r = requests.get(url='http://%s' % conn, headers=header)
    except Exception as e:
        print(f'Failed to GET data from {conn} (Error: {e})')
    else:
        if int(r.status_code) != 200:
            print(f'Failed to GET data from {conn} (Network Error: {r.status_code})')
        else:
            try:
                return r.json()
            except:
                return r.text

def __put_content(conn:str, db_name:str, table_name:str, payload):
    headers = {
        'type': 'json',
        'dbms': db_name,
        'table': table_name,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }
    try:
        r = requests.put(url='http://%s' % conn, headers=headers, data=json.dumps(payload))
    except Exception as e:
        print(f'Failed to PUT data against {conn} (Error: {e})')
    else:
        if int(r.status_code) != 200:
            print(f'Failed to PUT data against {conn} (Network Error: {r.status_code})')

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--conn', type=str, default='127.0.0.1:32349', help='REST conn to  GET data')
    parse.add_argument('--db-name', type=str, default='fleet_command', help='logical database name')
    args = parse.parse_args()

    conns = args.conn.split(',')

    raw_content = __get_command(conn=random.choice(conns), query='blockchain get (master, operator, query) bring.json [] [*][name] [*][ip] [*][rest_port]')
    blockchain_params = ast.literal_eval(raw_content)

    for i in range(1440):
        for table in COMMANDS:
            timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            for policy in blockchain_params:
                conn = f"127.0.0.1:{policy['rest_port']}"
                payload = {'timestamp': timestamp, 'node': policy['name'], 'ip': policy['ip']}
                raw_content = __get_command(conn=conn, query=COMMANDS[table])
                content = raw_content.split('(')[1].split(')')[0].replace(' ', '').split(',')
                for param in content:
                    payload[param.split('=')[0]] = ast.literal_eval(param.split('=')[-1])
                __put_content(conn=random.choice(conns), db_name=args.db_name, table_name=table, payload=payload)
            time.sleep(60)


if __name__ == '__main__':
    main()