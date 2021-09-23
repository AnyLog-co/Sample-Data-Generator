import argparse
import datetime 
import json 
import requests 
import time 

from protocols.rest_protocol import post_data

def get_data(url:str, token:str)->dict:
    """
    Get data from linode
    :args:
        url:str - URL to get data from 
        token:str - REST linode API Token 
    :params: 
        output:dict - data from GEt request 
    :return: 
        output 
    """
    try:
        #r = requests.get('https://api.linode.com/v4/linode/instances?data', headers={'Authorization': 'Bearer %s' % token}) 
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

def __extract_nodes(data:list)->dict:
    """
    Using data from Linode API extract node names and ids 
    :args: 
        data:str - data to extract info from
    :param: 
        nodes:dict - node_name:node_id
    :return: 
        nodes
    """
    nodes = {} 
    for node in data: 
        if 'demo' in node['tags'] and isinstance(node, dict): 
            if 'label' in list(node.keys()) and 'id' in list(node.keys()):
                nodes[node['label']] = node['id'] 
    return nodes 

def cpu_insight(node:str, data:list, dbms:str, timestamp:str)->list: 
    """
    Calculate CPU
    :args:
        node:str - node name 
        data:list - data for specific node 
        dbms:str - database name 
        table:str -  table name 
    :param: 
        cpu:list  - CPU data 
        data:dict - data to POST 
    :return: 
        data 
    """
    insight = [] 
    for row in data: 
        insight.append(row[-1])
    data = { 
        'dbms': dbms, 
        'table': 'cpu_insight', 
        'node': node,
        'timestamp': timestamp, 
        'value': sum(insight)/len(insight) 
    }
    #return data 
    return __convert_json(data) 

def io_insight(node:str, data:list, dbms:str, timestamp:str)->list: 
    """
    Swap data 
    :args:
        node:str - node name 
        data:list - data for specific node 
        dbms:str - database name 
        table:str -  table name 
    :param: 
        cpu:list  - CPU data 
        data:dict - data to POST 
    :return: 
        data 
    """
    insight = [] 
    for row in data: 
        insight.append(row[0])

    data = { 
        'dbms': dbms, 
        'table': 'io_swap_insight', 
        'node': node,
        'timestamp': timestamp, 
        'value': sum(insight)/len(insight) 
    }
    return __convert_json(data) 


def process(token:str, dbms:str)->list: 
    """
    Call to get data
    """
    output = get_data('https://api.linode.com/v4/linode/instances?data', token) 
    if isinstance(output, dict) and 'data' in list(output.keys()):
        nodes = __extract_nodes(output['data']) 
    if isinstance(nodes, dict) and nodes != {}: 
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {} 
        for node in list(nodes.keys()):
            output = get_data('https://api.linode.com/v4/linode/instances/%s/stats' % nodes[node], token) 
            for key in list(output['data'].keys()):
                if key == 'cpu': 
                    value = cpu_insight(node, output['data'][key], dbms, timestamp)
                elif key == 'io': 
                    value = io_insight(node, output['data'][key]['swap'], dbms, timestamp)
                if key in ['cpu', 'io']: 
                    if key not in data: 
                        data[key] = []
                    data[key].append(value) 

    return data 

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
    :sample: 
    {"table": "io_swap_insight", "node": "anylog-query", "dbms": "dmci", "value": 1626595200000.0, "timestamp": "2021-07-18 20:0017.397818"}    

    run mqtt client where broker=rest and user-agent = anylog and topic=(name=machine and dbms="bring [dbms]" and table="bring [table]" and column.timestamp.timestamp="bring [timestamp]" and column.node.str="bring [node]" and column.value.float="bring [value]") 

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
            data = process(token=args.token, dbms=args.dbms)
            for key in data: 
                for row in data[key]: 
                    post_data(conn=args.conn, data=row)
            time.sleep(args.sleep) 
    for i in range(args.iteration): 
        data = process(token=args.token, dbms=args.dbms)
        for key in data: 
            for row in data[key]: 
                post_data(conn=args.conn, data=row)
        time.sleep(args.sleep) 

if __name__ == '__main__':
    main() 
