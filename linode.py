import argparse
import datetime 
import json 
import requests 
import time 

def get_data(token:str)->dict:
    """
    Get data from linode
    :args:
        token:str - REST linode API Token 
    :params: 
        output:dict - data from GEt request 
    :return: 
        output 
    :sample-data:
    {
        'region': 'ap-south', 
        'specs': {
            'disk': 25600, 'memory': 1024, 'transfer': 1000, 
            'gpus': 0, 'vcpus': 1
        }, 
        'hypervisor': 'kvm', 'label': 'lsl-publisher', 'created': '2020-02-28T03:56:40', 
        'alerts': {
            'transfer_quota': 80, 'network_in': 10, 'io': 10000, 'network_out': 10, 'cpu': 90
        }, 
        'image': 'linode/ubuntu16.04lts', 'tags': ['demo'], 'id': 19564453, 'type': 'g6-nanode-1', 
        'watchdog_enabled': True, 'ipv4': ['172.104.180.110'], 'ipv6': '2400:8901::f03c:92ff:fee5:d553/128', 
        'status': 'running', 'group': '', 
        'backups': {
            'enabled': False, 
            'schedule': {
                'day': None, 'window': None
            }, 
            'last_successful': None
        }, 
        'updated': '2021-03-26T17:59:19'
    } 
    """
    try:
        r = requests.get('https://api.linode.com/v4/linode/instances?data', headers={'Authorization': 'Bearer %s' % token}) 
    except Exception as e: 
        print('Failed to GET data from linode (Error: %s)' % e)
        output = None
    else: 
        if r.status_code != 200: 
            print('Fialed to GET data form linode due to network error: %s' % str(r.status_code)) 
            output = None 
        else: 
            try: 
                output = r.json()
            except: 
                output = r.text
    return output

def __convert_json(data:list)->str:
    """
    Convert list to JSON 
    :args: 
        data:list - data to convert 
    :return: 
        data converted as JSON, if fails None 
    """
    try: 
        return json.dumps(data) 
    except Exception as e: 
        print('Failed to convert data to JSON format (Error: %s)' % e)
        return None  

def post_data(conn:str, data:dict):
    """
    Send data to AnyLog 
    :args: 
        conn:str - AnyLog REST IP & Port 
        data:list - list to send into AnyLog
    :params: 
        headers:dict - AnyLog headers 
        jdata:str - JSON conversion of 
    :return: 
        nothing is returned. however if something fails message is printed
    """
    headers = {
        'Content-Type': 'text/plain',
        'command': 'data',
        'User-Agent': 'AnyLog/1.23'
    }
    jdata = __convert_json(data) 
    if jdata != None: 
        try: 
            r = requests.post('http://%s' % conn, headers=headers, data=jdata)
        except Exception as e: 
            print('Failed to POST data to %s (Error: %s)' % (conn, e))
        else: 
            if r.status_code != 200: 
                print('Failed to POST data to %s due to network error: %s' % (conn, r.status_code))
      
def useage(data:list, dbms:str)->list: 
    """
    Extract useage config from GET result set 
    :args: 
        data:list - data from GET request 
        dbms:str - database to store data in
    :param: 
        rows:list - list of JSON dict objects to AnyLog
    :return: 
        rows
    :mqtt-call:
    # To execute within file, MQTT call should be within 1 line without "<" or ">" 
    <run mqtt client where broker=rest and user-agent=anylog and log=false and topic=(
        name=anylog and dbms="bring [dbms]" and table="bring [table]" and 
        column.timestamp.timestamp="bring [timestamp]" and 
        column.node_id.int="bring [node_id]" and
        column.node_name.str="bring [node_name]" and 
        column.value.float="bring [value]" 
    )> 
    # This example is based on the commented out row 
    <run mqtt client where broker=rest and user-agent=anylog and log=false and topic=(
        name=anylog and dbms="bring [dbms]" and table="bring [table]" and 
        column.timestamp.timestamp="bring [timestamp]" and 
        column.node_id.int="bring [node_id]" and
        column.node_name.str="bring [node_name]" and 
        column.disk_io.float="bring [io]" and 
        column.cpu.float="bring [cpu]" and 
        column.network_in.float="bring [network_in]" and 
        column.network_out.float="bring [network_out]" and 
        column.transfer_quota.float="bring [transfer_quota]"
    )> 
    """
    rows = [] 
    rows.append({
                'dbms': dbms, 
                'table': 'mahine_useage', 
                'timestamp': node['updated'],
                'node_id': node['id'], 
                'node_name': node['label'],
                'io': node['alerts']['io'], 
                'cpu': node['alerts']['cpu'], 
                'network_in': node['alerts']['network_in'],
                'network_out': node['alerts']['network_out'],
                'transfer_quota': node['alerts']['transfer_quota']
    })
    return rows

def disk_io(data:list, dbms:str): 
    rows = []
    for node in data: 
        if 'demo' in node['tags'] and isinstance(node, dict): 
            row = {
                'dbms': dbms, 
                'table': None, 
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                'node_name': 'unknown',
                'node_id': 0, 
                'value': None
            } 
            if 'updated' in list(node.keys()):
                row['timestamp'] = node['updated']
            if 'id' in list(node.keys()):
                row['node_id'] = node['id']
            if 'label' in list(node.keys()):
                row['node_name'] = node['label'] 
            if 'io' in node['alerts']:
                row['table'] = 'disk_io'
                row['value'] = node['alerts']['io'] 
                rows.append(row) 

    return rows

def cpu_usage(data:list, dbms:str): 
    rows = []
    for node in data: 
        if 'demo' in node['tags'] and isinstance(node, dict): 
            row = {
                'dbms': dbms, 
                'table': None, 
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                'node_name': 'unknown',
                'node_id': 0, 
                'value': None
            } 
            if 'updated' in list(node.keys()):
                row['timestamp'] = node['updated']
            if 'id' in list(node.keys()):
                row['node_id'] = node['id']
            if 'label' in list(node.keys()):
                row['node_name'] = node['label'] 
            if 'cpu' in node['alerts']:
                row['table'] = 'cpu_useage'
                row['value'] = node['alerts']['cpu'] 
                rows.append(row) 



    return rows
 
def network_in(data:list, dbms:str): 
    rows = []
    for node in data: 
        if 'demo' in node['tags'] and isinstance(node, dict): 
            row = {
                'dbms': dbms, 
                'table': None, 
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                'node_name': 'unknown',
                'node_id': 0, 
                'value': None
            } 
            if 'updated' in list(node.keys()):
                row['timestamp'] = node['updated']
            if 'id' in list(node.keys()):
                row['node_id'] = node['id']
            if 'label' in list(node.keys()):
                row['node_name'] = node['label'] 
            if 'network_in' in node['alerts']:
                row['table'] = 'network_in'
                row['value'] = node['alerts']['network_in'] 
                rows.append(row) 
    return rows 
  
def network_out(data:list, dbms:str): 
    rows = []
    for node in data: 
        if 'demo' in node['tags'] and isinstance(node, dict): 
            row = {
                'dbms': dbms, 
                'table': None, 
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                'node_name': 'unknown',
                'node_id': 0, 
                'value': None
            } 
            if 'updated' in list(node.keys()):
                row['timestamp'] = node['updated']
            if 'id' in list(node.keys()):
                row['node_id'] = node['id']
            if 'label' in list(node.keys()):
                row['node_name'] = node['label'] 
            if 'network_out' in node['alerts']:
                row['table'] = 'network_out'
                row['value'] = node['alerts']['network_out'] 
                rows.append(row) 
    return rows  
  
def transfer_quota(data:list, dbms:str): 
    rows = []
    for node in data: 
        if 'demo' in node['tags'] and isinstance(node, dict): 
            row = {
                'dbms': dbms, 
                'table': None, 
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                'node_name': 'unknown',
                'node_id': 0, 
                'value': None
            } 
            if 'updated' in list(node.keys()):
                row['timestamp'] = node['updated']
            if 'id' in list(node.keys()):
                row['node_id'] = node['id']
            if 'label' in list(node.keys()):
                row['node_name'] = node['label'] 
 
            if 'transfer_quota' in node['alerts']:
                row['table'] = 'transfer_quota'
                row['value'] = node['alerts']['transfer_quota'] 
                rows.append(row) 
 
    return rows 

def main(): 
    """
    Using the linode cURL API extract information regarding our network
    :positional arguments:
        conn                  AnyLog REST IP & Port to send data to 	[default: 172.104.180.110:2049]
        token                 Linode token node				[default: ab21f3f79e22693bb33815772fd6a48fa91a0298e9052be0250a56fec7b4cc70] 
        dbms                  Database to store data in			[default: test] 
    :optional arguments:
        -h, --help            			show this help message and exit
        -i, --iteration 	ITERATION	number of iterations. if set to 0 run continuesly	(default: 1)
        -s, --sleep 		SLEEP		wait between insert 					(default: 0)
    :params: 
        i:int - iteration counter 
        output:list - raw content from get_data 
        send_data:list - extracted data to send into AnyLog
    :URL: 
    https://www.linode.com/docs/api/
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('conn',  type=str,  default='172.104.180.110:2049',                                             help='AnyLog REST IP & Port to send data to')
    parser.add_argument('token', type=str,  default='ab21f3f79e22693bb33815772fd6a48fa91a0298e9052be0250a56fec7b4cc70', help='Linode token node') 
    parser.add_argument('dbms',  type=str,  default='test',                                                             help='Database to store data in') 
    parser.add_argument('-i', '--iteration', type=int,   default=1,                              help='number of iterations. if set to 0 run continuesly')
    parser.add_argument('-s', '--sleep',     type=float, default=0,                              help='wait between insert')
    args = parser.parse_args()
      
    if args.iteration == 0: 
        while True: 
            output = get_data(args.token) 
            if 'data' in list(output.keys()): 
                data = output['data']
                send_data = disk_io(data=data, dbms=args.dbms)
                post_data(conn=args.conn, data=send_data) 
                send_data = cpu_usage(data=data, dbms=args.dbms) 
                post_data(conn=args.conn, data=send_data) 
                send_data = network_in(data=data, dbms=args.dbms) 
                post_data(conn=args.conn, data=send_data) 
                send_data = network_out(data=data, dbms=args.dbms)
                post_data(conn=args.conn, data=send_data) 
                send_data =transfer_quota(data=data, dbms=args.dbms) 
                post_data(conn=args.conn, data=send_data) 
            time.sleep(args.sleep) 


    for i in range(args.iteration):
        output = get_data(args.token) 
        print(output) 
        if 'data' in list(output.keys()) and isinstance(output, dict): 
            data = output['data']
            send_data = disk_io(data=data, dbms=args.dbms)
            post_data(conn=args.conn, data=send_data) 
            send_data = cpu_usage(data=data, dbms=args.dbms) 
            post_data(conn=args.conn, data=send_data) 
            send_data = network_in(data=data, dbms=args.dbms) 
            post_data(conn=args.conn, data=send_data) 
            send_data = network_out(data=data, dbms=args.dbms)
            post_data(conn=args.conn, data=send_data) 
            send_data =transfer_quota(data=data, dbms=args.dbms) 
            post_data(conn=args.conn, data=send_data) 
 
            time.sleep(args.sleep) 

if __name__ == '__main__':
    main() 
