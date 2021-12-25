import argparse
import datetime 
import json 
import requests 
import time 

def get_data(url:str, token:str)->dict:
    """
    Get data from linode
    :args:
        url:str - URL to get data from 
        token:str - REST linode API Token 
    :params: 
        output:dict - data from GET request
    :return: 
        output 
    """
    try:
        r = requests.get(url, headers={'Authorization': 'Bearer %s' % token}) 
    except Exception as e: 
        print('Failed to GET data from linode (Error: %s)' % e)
        output = None
    else: 
        if r.status_code != 200: 
            print('Failed to GET data form linode due to network error: %s' % str(r.status_code)) 
            output = None 
        else: 
            try: 
                output = r.json()
            except: 
                output = r.text
    return output


def node_machine_info(data:list, tag:str, timestamp:str=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))->(list, list):
    """
    Generate machine information for a specific tag
    :args:
        data:list - data for linode servers
        tag:str - tag to group of servers to check
        timestamp:str - timestamp
    :params:
        payloads:list - list of machine information
        machines:list - list of machine IDs
    :return:
        payloads, machines
    """
    payloads = []
    machines = []
    for row in data:
        if tag in row['tags']:
            payload = {
                'timestamp': timestamp,
                'machine_id': row['id'],
                'name': row['label'],
                'ip': row['ipv4'][0],
                'local_ip': row['ipv4'][0],
                'ipv6': row['ipv6'],
                'region': row['region']
            }
            if len(row['ipv4']) > 1:
                payload['local_ip'] = row['ipv4'][1]
            machines.append(row['id'])
            payloads.append(payload)

    return payloads, machines


def node_config_info(data:list, tag:str, timestamp:str=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))->list:
    """
    Generate general informaton regarding the node
    :args:
        data:list - data for linode servers
        tag:str - tag to group of servers to check
        timestamp:str - timestamp
    :params:
        payloads:list - list of machine information
    :return:
        payloads
    """
    payloads = []
    for row in data:
        if tag in row['tags']:
            payloads.append({
                'timestamp': timestamp,
                'create_ts': row['created'],
                'update_ts': row['updated'],
                'machine_id': row['id'],
                'status': row['status'],
                'disk': row['specs']['disk'],
                'memory': row['specs']['memory'],
                'vcpus': row['specs']['vcpus'],
                'gpus': row['specs']['gpus'],
                'transfer': row['specs']['transfer']
            })
    return payloads


def extract_insight(data:list, member_id:str, timestamp:str=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))->list:
    """
    Extract insight for either (disk) IO or CPU usage
    :arg:
        data:list - list of values
        member_id:str - member correlated to values
        timestamp:str - timestamp
    :params:
        insight:list - extracted list of values
    :return:
        payload with values timestamp, member_id and value
    """
    insight = []
    for row in data:
        insight.append(row[-1])

    return {
        'timestamp': timestamp,
        'membber_id': member_id,
        'value': sum(insight) / len(insight)
    }


def extract_network_insight(data:list, member_id:str, timestamp:str=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))->list:
    """
    Extract network insight
    :arg:
        data:list - list of network values
        member_id:str - member correlated to values
        timestamp:str - timestamp
    :params:
        insight:list - extracted list of values
    :return:
        payload with values timestamp, member_id and value
    """
    values = {'in': [], 'out': []}
    for key in ['in', 'out']:
        for row in data[key]:
            values[key].append(row[-1])

    return {
        'member_id': member_id,
        'timestamp': timestamp,
        'value': sum(values['in']) / (sum(values['in']) + sum(values['out']))
    }

def linode(token:str, tag:str='demo', initial_configs:bool=False):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    payloads = {
        'node_config': [],
        'node_summary': [],
        'cpu_insight': [],
        'io_insight': [],
        'netv4_public_insight': [],
        'netv6_public_insight': []
    }
    data = get_data(url='https://api.linode.com/v4/linode/instances', token=token)

    # machine(s) summary
    payloads['node_config'], machines = node_machine_info(data=data['data'], tag=tag, timestamp=timestamp)
    payloads['node_summary'] = node_config_info(data=data['data'], tag=tag, timestamp=timestamp)
    if initial_configs is False:
        del payloads['node_config']
        del payloads['node_summary']

    for machine in machines:
        data = get_data('https://api.linode.com/v4/linode/instances/%s/stats' % machine, token)
        payloads['cpu_insight'].append(extract_insight(data=data['data']['cpu'], member_id=machine, timestamp=timestamp))
        payloads['io_insight'].append(extract_insight(data=data['data']['io']['io'], member_id=machine, timestamp=timestamp))
        payloads['netv4_public_insight'].append(extract_network_insight(data=data['data']['netv4'], member_id=machine, timestamp=timestamp))
        payloads['netv6_public_insight'].append(extract_network_insight(data=data['data']['netv6'], member_id=machine, timestamp=timestamp))

    return payloads


if __name__ == '__main__':
    # main()
    linode('ab21f3f79e22693bb33815772fd6a48fa91a0298e9052be0250a56fec7b4cc70')