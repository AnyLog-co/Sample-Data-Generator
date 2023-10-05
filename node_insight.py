import argparse
import datetime
import json
import re
import requests
import concurrent.futures


class Snetio:
    """
    Convert snetio from string to JSON format
    """
    def __init__(self, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        self.bytes_sent = int(bytes_sent)
        self.bytes_recv = int(bytes_recv)
        self.packets_sent = int(packets_sent)
        self.packets_recv = int(packets_recv)
        self.errin = int(errin)
        self.errout = int(errout)
        self.dropin = int(dropin)
        self.dropout = int(dropout)

def __generic_get_cmd(conn:str, headers:dict):
    """
    Execute GET command via REST
    :args:
        conn:str - URL to run against
        headers:dict - REST Headers
    :params:
        output - output
        r:requests.GET - rest request result
    :return:
        output
    """
    output = None
    try:
        r = requests.get(url=f"http://{conn}", headers=headers, timeout=30, auth=())
    except Exception as err:
        print(f"Failed to execute {headers['command']} against {conn} (Error: {err})")
    else:
        if int(r.status_code) != 200:
            print(f"Failed to execute {headers['command']} against {conn} (Network Error: {r.status_code})")
        else:
            try:
                output = r.json()
            except:
                output = r.text

    return output

def __publish_data(conn:str, dbms:str, table:str, data:list):
    headers = {
        'type': 'json',
        'dbms': dbms,
        'table': table,
        'mode': "streaming",
        'Content-Type': 'text/plain'
    }

    payload = json.dumps(data)
    try:
        r = requests.put(url=f"http://{conn}", headers=headers, timeout=30, aut=(), data=payload)
    except Exception as error:
        print(f"Failed to push data into {conn} via PUT (Error: {error})")
    else:
        if int(r.status_code) != 200:
            print(f"Failed to push data into {conn} via PUT (Network Error: {r.status_code})")


def blockchain_get(conn:str):
    """
    Get connection information from blockchain
    :args:
        conn:str - REST connection information
    :params:
        policies:dict - content from blockchain
        headers:dict - REST headers
    :return:
        policies
    """
    policies = {}
    headers = {
        "command": "blockchain get (master, query, operator)",
        "User-Agent": "AnyLog/1.23"
    }

    raw_policies = __generic_get_cmd(conn=conn, headers=headers)
    if isinstance(raw_policies, list):
        for policy in raw_policies:
            policy_type = list(policy)[0]
            policies[policy[policy_type]['name']] = {
                'type': policy_type,
                'conn': f"{policy[policy_type]['ip']}:{policy[policy_type]['rest_port']}"
            }
    return policies


def __get_disk_usage(conn:str):

    headers = {
        "command": "get disk percentage .",
        "User-Agent": "AnyLog"
    }

    return __generic_get_cmd(conn=conn, headers=headers)

def __get_cpu_usage(conn:str):
    headers = {
        "command": "get node info cpu_percent",
        "User-Agent": "AnyLog"
    }

    return __generic_get_cmd(conn=conn, headers=headers)


def __network_io(conn:str):
    """
    snetio(bytes_sent=1150305807, bytes_recv=4758743346, packets_sent=4439344, packets_recv=5487649, errin=0, errout=0, dropin=0, dropout=0)
    """
    snetio_obj = None
    output = {}
    headers = {
        "command": "get node info net_io_counters",
        "User-Agent": "AnyLog/1.23"
    }

    snetio_str = __generic_get_cmd(conn=conn, headers=headers)
    pattern = r"snetio\((.*?)\)"
    matches = re.search(pattern, snetio_str)
    if matches:
        values = matches.group(1).split(', ')
        values_dict = {}
        for value in values:
            key, val = value.split('=')
            values_dict[key.strip()] = val.strip()

        # Create a snetio object with the parsed values
        snetio_obj = Snetio(**values_dict)

    if snetio_obj is not None:
        output = {
            "bytes_transferred": snetio_obj.bytes_recv + snetio_obj.bytes_sent,
            "packet_ratio": round(snetio_obj.packets_sent / (snetio_obj.packets_sent + snetio_obj.packets_recv), 3),
            "bytes_per_packet_sent": round(snetio_obj.bytes_sent/snetio_obj.packets_sent, 3),
            "errors": snetio_obj.errin + snetio_obj.errout + snetio_obj.dropin + snetio_obj.dropout
        }
    return output



def node_insight(blockchain_policies:dict):
    disk_usage = []
    cpu_usage = []
    network_usage = []
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def get_disk_space(policy_name:str, policy_info:dict, disk_values:float):
        return {
            "timestamp": timestamp,
            "name": policy_name,
            "node_type": policy_info['type'],
            "ip_address": policy_info['conn'].split(":")[0],
            "value": disk_values
        }

    def get_cpu_usage(policy_name:str, policy_info:dict, cpu_value:float):
        return {
            "timestamp": timestamp,
            "name": policy_name,
            "node_type": policy_info['type'],
            "ip_address": policy_info['conn'].split(":")[0],
            "value": cpu_value
        }

    def get_network_insight(policy_name:str, policy_info:dict, network_insight:dict):
        return {
            "timestamp": timestamp,
            "name": policy_name,
            "node_type": policy_info['type'],
            "ip_address": policy_info['conn'].split(":")[0],
            **network_insight
        }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        disk_futures = {policy_name: executor.submit(__get_disk_usage, conn=policy_info['conn'])
                   for policy_name, policy_info in blockchain_policies.items()}
        cpu_futures = {policy_name: executor.submit(__get_cpu_usage, conn=policy_info['conn'])
                       for policy_name, policy_info in blockchain_policies.items()}
        network_future = {policy_name: executor.submit(__network_io, conn=policy_info['conn'])
                       for policy_name, policy_info in blockchain_policies.items()}

        for policy_name, future in disk_futures.items():
            disk_usage_value = future.result()
            disk_usage.append(get_disk_space(policy_name=policy_name, policy_info=blockchain_policies[policy_name],
                                             disk_values=disk_usage_value))
        for policy_name, future, in cpu_futures.items():
            cpu_usage_value = future.result()
            cpu_usage.append(get_cpu_usage(policy_name=policy_name, policy_info=blockchain_policies[policy_name],
                                           cpu_value=cpu_usage_value))
        for policy_name, future in network_future.items():
            network_insight_values = future.result()
            network_usage.append(get_network_insight(policy_name=policy_name,
                                                     policy_info=blockchain_policies[policy_name],
                                                     network_insight=network_insight_values))

    return disk_usage, cpu_usage, network_usage


# def publish_data(conn, dbms, table, data):
#     def publish_data_task():
#         __publish_data(conn=conn, dbms=dbms, table=table, data=data)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.submit(publish_data_task)

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('conn', type=str, help='REST connection information')
    parse.add_argument('dbms', type=str, help='logical database to store data in')
    args = parse.parse_args()

    policies = blockchain_get(conn=args.conn)
    disk_usage, cpu_usage, network_usage = node_insight(blockchain_policies=policies)

    __publish_data(conn=args.conn, dbms=args.dbms, table="disk_usage", data=disk_usage)
    __publish_data(conn=args.conn, dbms=args.dbms, table="cpu_usage", data=cpu_usage)
    __publish_data(conn=args.conn, dbms=args.dbms, table="network_insight", data=network_usage)

    

if __name__ == '__main__':
    main()
