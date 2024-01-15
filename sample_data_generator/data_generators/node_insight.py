import json
import time

from sample_data_generator.support.timestamp_generator import generate_timestamp
from sample_data_generator.publishing_protocols.anylog_rest import AnyLogREST

def __get_blockchain(anylog_conn:AnyLogREST):
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
    ip_list = {}
    for node_type in ["master", "query", "operator", "publisher"]:
        if node_type not in ip_list:
            ip_list[node_type] = []
        headers = {
            "command": f"blockchain get {node_type} bring.ip_port",
            "User-Agent": "AnyLog/1.23"
        }
        values = anylog_conn.get_data(headers=headers).split(",")
        for ip in values:
            ip_list[node_type].append(ip)

    return ip_list

def node_insight(anylog_conn:AnyLogREST, destination_ip:str):
    output = None
    headers = {
        "command": "get dictionary where format=json",
        "User-Agent": "AnyLog/1.23",
        "destination": destination_ip
    }

    r = anylog_conn.get_data(headers=headers)
    if destination_ip in r and 'node_insight' in r[destination_ip]:
        results = json.loads(r[destination_ip]['node_insight'])
        if isinstance(results, dict):
            if 'node name' in results and 'Node Name' in results:
                del results['Node Name']
            output = {key.lower().replace(" ", "_"): value for key, value in results.items()}

    return output


def get_node_insight(anylog_conn:AnyLogREST, db_name:str, row_count:int=1, sleep:float=30, timezone:str='utc', exception:bool=False)->list:

    ips_addresses = __get_blockchain(anylog_conn=anylog_conn)
    node_insights = []
    for i in range(row_count):
        timestamp = generate_timestamp(timezone=timezone, enable_timezone_range=False)
        for node_type in ips_addresses:
            for ip in ips_addresses[node_type]:
                output = node_insight(anylog_conn=anylog_conn, destination_ip=ip)
                if output is not None:
                    output['dbname'] = db_name
                    output['table'] = 'node_insight'
                    output['timestamp'] = timestamp
                    node_insights.append(output)
            if i < row_count - 1:
                time.sleep(sleep)

    return node_insights

