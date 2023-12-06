import datetime
import json
from src.publishing_protocols.rest_protocols import get_data

def __get_blockchain(conn:str, auth:tuple=(), timeout:int=30, exception:bool=False):
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
    for node_type in ["master", "query", "operator", "publisher"]:
        if node_type not in policies:
            policies[node_type] = None
        headers = {
            "command": f"blockchain get {node_type} bring.ip_port ",
            "User-Agent": "AnyLog/1.23"
        }
        policies[node_type] = get_data(conn=conn, headers=headers, auth=auth, timeout=timeout, exception=exception)

    return policies

def get_node_insight(conn:str, destination_ip:str, timestamp:str, auth=(), timeout=30, exception=True):
    output = None
    headers = {
        "command": "get dictionary where format=json",
        "User-Agent": "AnyLog/1.23",
        "destination": destination_ip
    }

    r = get_data(conn=conn, headers=headers, auth=auth, timeout=timeout, exception=exception)
    if destination_ip in r and 'node_insight' in r[destination_ip]:
        results = json.loads(r[destination_ip]['node_insight'])
        if isinstance(results, dict):
            if 'node name' in results and 'Node Name' in results:
                del results['Node Name']
            output = {key.lower().replace(" ", "_"): value for key, value in results.items()}
            output['timestamp'] = timestamp

    return output

def node_insight(conn:str, auth:tuple=(), timeout:int=30, exception:bool=False)->list:
    ips_addresses = __get_blockchain(conn=conn, auth=auth, timeout=timeout, exception=exception)
    node_insights = []
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    for ip in ips_addresses:
        print(ip)
        output = get_node_insight(conn=conn, destination_ip=ip, timestamp=timestamp, auth=auth, timeout=timeout,
                                  exception=exception)
        if output is not None:
            node_insights.append(output)
    return node_insights

#
# if __name__ == '__main__':
#     node_insight(conn="23.239.12.151:32349")

