import ast
import os
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('data_generators', 1)[0]
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, PROTOCOLS)
from support import generate_timestamp
from rest import get_command


def __get_blockchain(conn:str, auth:tuple=None, timeout:int=30, exception:bool=False)->list:
    """
    Get content from blockchain
    :args:
        conn:str - REST
        auth:tuple - Authentication username + password
        timeout:nt - wait time
        exception:bool - whether or not to print error messages
    """
    headers = {
        'command': 'blockchain get (master, operator, publisher, query) bring.json [*][name] [*][ip] [*][rest_port]',
        'User-Agent': 'AnyLog/1.23'
    }
    raw_response = get_command(conn=f'http://{conn}', headers=headers, auth=auth, timeout=timeout, exception=exception)
    if int(raw_response.status_code) == 200:
        try:
            content = raw_response.json()
        except Exception as e:
            try:
                content = ast.literal_eval(raw_response.text)
            except Exception as e:
                if exception is True:
                    print(f'Failed to extract results from {conn} (Error: {e})')
    elif exception is True:
        print(f'Failed to extract results from {conn} (Network Error: {raw_response.status_code}')
    return content

def network_io(conn:str, auth:tuple=None, timeout:int=30, exception:bool=False):
    headers = {
        'command': 'get node info net_io_counters',
        'User-Agent': 'AnyLog/1.23'
    }
    payloads = []
    blockchain_list = __get_blockchain(conn=conn, auth=auth, timeout=timeout, exception=exception)
    for node in blockchain_list:
        conn = f'{node["ip"]}:{node["rest_port"]}'
        raw_results = get_command(conn=f'http://{conn}', headers=headers, auth=auth, timeout=timeout, exception=exception)
        if raw_results is None and exception is True:
            print(f'Failed to execute GET against {conn}')
        elif int(raw_results.status_code) != 200 and exception is True:
            print(f'Failed to execute GET against {conn} (Network Error: {raw_results.status_code}')
        if int(raw_results.status_code) == 200:
            data = {'node': node['name'], 'ip': node['ip']}
            for param in raw_results.text.split('(')[-1].split(')')[0].split(', '):
                data[param.split('=')[0]] = int(param.split('=')[-1])
            payloads.append(data)
    print(payloads)

if __name__ == '__main__':
    network_io(conn='23.239.12.151:32349', exception=True)