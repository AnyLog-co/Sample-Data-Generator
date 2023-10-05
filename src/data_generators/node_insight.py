import re
import concurrent.futures

from src.publishing_protocols.rest_protocols import get_data
from src.data_generators.__support__ import Snetio



def __get_disk_usage(conn:str, auth:tuple=(), timeout:int=30, exception:bool=False):

    headers = {
        "command": "get disk percentage .",
        "User-Agent": "AnyLog"
    }

    return get_data(conn=conn, headers=headers, auth=auth, timeout=timeout, exception=exception)

def __get_cpu_usage(conn:str, auth:tuple=(), timeout:int=30, exception:bool=False):
    headers = {
        "command": "get node info cpu_percent",
        "User-Agent": "AnyLog"
    }

    return get_data(conn=conn, headers=headers, auth=auth, timeout=timeout, exception=exception)

def __network_io(conn:str, auth:tuple=(), timeout:int=30, exception:bool=False):
    """
    snetio(bytes_sent=1150305807, bytes_recv=4758743346, packets_sent=4439344, packets_recv=5487649, errin=0, errout=0, dropin=0, dropout=0)
    """
    snetio_obj = None
    output = {}
    headers = {
        "command": "get node info net_io_counters",
        "User-Agent": "AnyLog/1.23"
    }

    snetio_str = get_data(conn=conn, headers=headers, auth=auth, timeout=timeout, exception=exception)
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

def get_blockchain(conn:str, auth:tuple=(), timeout:int=30, exception:bool=False):
    """
    Execute a `blockchain get` to get a list of all nodes in the network
    :args:
        conn:str - REST connection information
        auth:tuple - REST authentication
        timeout:int - REST timeout
        exception:bool - Whether to print exceptions
    :params:
        policies:dict - formatted results from `blockchain get`
        headers:dict - REST headers
        raw_policies:list - raw results from REST request
    :return:
        policies
    """
    policies = {}
    headers = {
        "command": "blockchain get (master, query, operator, publisher)",
        "User-Agent": "AnyLog/1.23"
    }

    raw_policies = get_data(conn=conn, headers=headers, auth=auth, timeout=timeout, exception=exception)
    if isinstance(raw_policies, list) and raw_policies is not None:
        for policy in raw_policies:
            policy_type = list(policy)[0]
            policies[policy[policy_type]['name']] = {
                'type': policy_type,
                'conn': f"{policy[policy_type]['ip']}:{policy[policy_type]['rest_port']}"
            }
    return policies


def network_insight(conn:str, db_name:str, auth:tuple=(), timeout:int=30, exception:bool=False):
    nodes = get_blockchain(conn=conn, auth=auth, timeout=timeout, exception=exception)
    data = []


    def get_disk_space(policy_name: str, policy_info: dict, disk_values: float):
        return {
            "dbms": db_name,
            "table": "free_disk_space",
            "name": policy_name,
            "node_type": policy_info['type'],
            "ip_address": policy_info['conn'].split(":")[0],
            "value": disk_values
        }

    def get_cpu_usage(policy_name: str, policy_info: dict, cpu_value: float):
        return {
            "dbms": db_name,
            "table": "cpu_usage",
            "name": policy_name,
            "node_type": policy_info['type'],
            "ip_address": policy_info['conn'].split(":")[0],
            "value": cpu_value
        }

    def get_network_insight(policy_name: str, policy_info: dict, network_insight: dict):
        return {
            "dbms": db_name,
            "table": "network_insight",
            "name": policy_name,
            "node_type": policy_info['type'],
            "ip_address": policy_info['conn'].split(":")[0],
            **network_insight
        }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        disk_futures = {policy_name: executor.submit(__get_disk_usage, conn=policy_info['conn'])
                        for policy_name, policy_info in nodes.items()}
        cpu_futures = {policy_name: executor.submit(__get_cpu_usage, conn=policy_info['conn'])
                       for policy_name, policy_info in nodes.items()}
        network_future = {policy_name: executor.submit(__network_io, conn=policy_info['conn'])
                          for policy_name, policy_info in nodes.items()}

        for policy_name, future in disk_futures.items():
            disk_usage_value = future.result()
            data.append(get_disk_space(policy_name=policy_name, policy_info=nodes[policy_name],
                                             disk_values=disk_usage_value))
        for policy_name, future, in cpu_futures.items():
            cpu_usage_value = future.result()
            data.append(get_cpu_usage(policy_name=policy_name, policy_info=nodes[policy_name],
                                           cpu_value=cpu_usage_value))
        for policy_name, future in network_future.items():
            network_insight_values = future.result()
            data.append(get_network_insight(policy_name=policy_name,
                                                     policy_info=nodes[policy_name],
                                                     network_insight=network_insight_values))

    return data





