import argparse
import datetime 
import json 
import requests 
import time 

#from protocols.rest_protocol import post_data
from protocols.rest_protocol import send_data

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
        'command': 'data',
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }
    print(data)
    """
    try:
        r = requests.post('http://%s' % conn, headers=headers, data=data)
    except Exception as e:
        print('Failed to POST data to %s (Error: %s)' % (conn, e))
    else:
        if r.status_code != 200:
           print('Failed to POST data to %s due to network error: %s' % (conn, r.status_code))
    """

def put_data(conn:str, data:dict):
    dbms = data['dbms']
    del data['dbms']
    table = data['table']
    del data['table']
    send_data(payloads=data, conn=conn, dbms=dbms, table_name=table, mode='streaming')

def node_machine_info(dbms:str, data:list)->list:
    """
    Based on information in data, create JSON object of information regarding the node
        * machine_id
        * machine name
        * IP addresses
        * region
    :args:
        dbms:str - databas name
        data:list - list of rows extracted using Linode API
    :params:
        node_config:dict - extracted node configuration information
        node_config_list:list - list of node_config objects
    :return:
        node_config_list
    """
    node_config_list = []

    for row in data:
        node_config = {
            'dbms': dbms,
            'table': 'node_config',
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'machine_id': None,
            'name': None,
            'ip': None,
            'local_ip': None,
            'ipv6': None,
            'region': None
        }
        if 'demo' in row['tags']:
            node_config['machine_id'] = row['id']
            node_config['name'] = row['label']
            node_config['ip'] = row['ipv4'][0]
            node_config['local_ip'] = row['ipv4'][0]
            if len(row['ipv4']) > 1:
                node_config['local_ip'] = row['ipv4'][1]
            node_config['ipv6'] = row['ipv6']
            node_config['region'] = row['region']

            node_config_list.append(node_config)
    return node_config_list


def node_config_info(dbms:str, machine_ids:list, data:list)->list:
    """
    Based on information in data, create JSON object of information regarding the node
        * machine_id
        * status
        * create_ts
        * update_ts
        * disk
        * memory
        * vCPU
        * gCPU
        * transfer
    :args:
        dbms:str - database name
        data:list - list of rows extracted using Linode API
        tag
    :params:
        node_summary:dict - extracted node configuration information
        node_summary_list:list - list of node_config objects
    :return:
        node_config_list
    """
    node_summary_list = []
    for row in data:
        node_summary = {
            'dbms': dbms,
            'table': 'node_config',
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'machine_id': None,
            'status': None,
            'create_ts': None,
            'update_ts': None,
            'disk': None,
            'memory': None,
            'vcpus': None,
            'gpus': None,
            'transfer': None
        }
        if row['id'] in machine_ids:
            node_summary['machine_id'] = row['id']
            node_summary['status'] = row['status']
            node_summary['create_ts'] = row['created']
            node_summary['update_ts'] = row['updated']
            node_summary['disk'] = row['specs']['disk']
            node_summary['memory'] = row['specs']['memory']
            node_summary['vcpus'] = row['specs']['vcpus']
            node_summary['gpus'] = row['specs']['gpus']
            node_summary['transfer'] = row['specs']['transfer']
            node_summary_list.append(node_summary)

    return  node_summary_list


def extract_insight(dbms:str, table:str, member_id:int, timestamp:str, data:list)->dict:
    """
    Generate JSON object from data
    :args:
        dbms:str - database to store data in
        member_id:int - node member ID
        timestamp:str - timestamp value
        data:list - data to use
    :params:
        insight:list - sublist from data
        json_data:dict - Dictionary object of data
    :return:
        json_data
    """
    insight = []
    if table == 'cpu_insight':
        for row in data:
            insight.append(row[-1])
    else:
        for row in data:
            insight.append(row[0])

    return {
        'dbms': dbms,
        'table': table,
        'member_id': member_id,
        'timestamp': timestamp,
        'value': sum(insight) / len(insight)
    }


def extract_network_insight(dbms:str, table:str, member_id:int, timestamp:str, private_data_in:list,
                            private_data_out:list, public_data_in:list, public_data_out:list)->dict:
    """
    Generate JSON object from data for network information
    :args:
        dbms:str - database to store data in
        member_id:int - node member ID
        timestamp:str - timestamp value
        private_data_in:list - private network data in
        private_data_out:list - private network data out
        public_data_in:list - public network data in
        public_data_out:list - public network data out
    :params:
        insight:list - sublist from data
        json_data:dict - Dictionary object of data
    :return:
        json_data
    """
    private_data = {'in': [], 'out': []}
    public_data = {'in': [], 'out': []}
    for row in private_data_in:
        private_data['in'].append(row[0])
    for row in private_data_out:
        private_data['out'].append(row[0])

    for row in public_data_in:
        public_data['in'].append(row[-1])
    for row in public_data_out:
        public_data['out'].append(row[-1])

    return {
        'dbms': dbms,
        'table': table,
        'member_id': member_id,
        'timestamp': timestamp,
        'public_in': sum(public_data['in'])/len(public_data['in']),
        'public_out': sum(public_data['out'])/len(public_data['out']),
        'private_in': sum(private_data['in'])/len(private_data['in']),
        'private_out': sum(private_data['out'])/len(private_data['out']),
    }

def data_generator(conn:str, token:str, machine_ids:list, dbms:str):
    """
    Generate data
    :args:
        conn:str - IP & Port REST information
        token:str - Linode API token
        machiine_ids:list - list of IDs
        dbms:str - database name
    :params:
        timestamp:str - timestamp value
        output:list - raw stats for a given machine_id
        cpu_info:dict - CPU data
        swap_info:dict - swap info
        io_info:dict - read/write stats
        netv4_info:dict - network v4 info
        netv6_info:dict - network v6 info
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    for machine_id in machine_ids:
        output = get_data('https://api.linode.com/v4/linode/instances/%s/stats' % machine_id, token)

        cpu_info = extract_insight(dbms=dbms, table='cpu_insight', member_id=machine_id, timestamp=timestamp,
                                   data=output['data']['cpu'])
        swap_info = extract_insight(dbms=dbms, table='swap_insight', member_id=machine_id, timestamp=timestamp,
                                    data=output['data']['io']['swap'])
        io_info = extract_insight(dbms=dbms, table='io_insight', member_id=machine_id, timestamp=timestamp,
                                  data=output['data']['io']['io'])
        netv4_info = extract_network_insight(dbms=dbms, table='netv4_insight', member_id=machine_id,
                                             timestamp=timestamp, private_data_in=output['data']['netv4']['private_in'],
                                             private_data_out=output['data']['netv4']['private_out'],
                                             public_data_in=output['data']['netv4']['in'],
                                             public_data_out=output['data']['netv4']['out'])
        netv6_info = extract_network_insight(dbms=dbms, table='netv6_insight', member_id=machine_id,
                                             timestamp=timestamp, private_data_in=output['data']['netv6']['private_in'],
                                             private_data_out=output['data']['netv6']['private_out'],
                                             public_data_in=output['data']['netv6']['in'],
                                             public_data_out=output['data']['netv6']['out'])
        put_data(conn=conn, data=cpu_info)
        put_data(conn=conn, data=io_info)
        put_data(conn=conn, data=swap_info)
        put_data(conn=conn, data=netv4_info)
        put_data(conn=conn, data=netv6_info)


def main():
    """
    Using the linode cURL API extract information regarding our network
    :positional arguments:
        conn                  AnyLog REST IP & Port to send data to 	[default: 172.104.180.110:2049]
        token                 Linode token node				[default: ab21f3f79e22693bb33815772fd6a48fa91a0298e9052be0250a56fec7b4cc70] 
        dbms                  Database to store data in			[default: test] 
    :optional arguments:
        -h, --help            			show this help message and exit
        -i, --iteration 	ITERATION	number of iterations. if set to 0 run continuously	(default: 1)
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
    parser.add_argument('-i', '--iteration', type=int,   default=1,                              help='number of iterations. if set to 0 run continuously')
    parser.add_argument('-s', '--sleep',     type=float, default=0,                              help='wait between insert')
    args = parser.parse_args()
    machine_ids = []
    data = get_data(url='https://api.linode.com/v4/linode/instances', token=args.token)
    machine_info_list = node_machine_info(dbms=args.dbms, data=data['data'])
    for row in machine_info_list:
        machine_ids.append(row['machine_id'])
        put_data(conn=args.conn, data=row)

    config_info_list = node_config_info(dbms=args.dbms, machine_ids=machine_ids, data=data['data'])
    for row in config_info_list:
        put_data(conn=args.conn, data=row)

    if args.iteration == 0:
        while True:
            data_generator(conn=args.conn, token=args.token, machine_ids=machine_ids, dbms=args.dbms)
            time.sleep(args.sleep)

    for i in range(args.iteration):
        data_generator(conn=args.conn, token=args.token, machine_ids=machine_ids, dbms=args.dbms)
        time.sleep(args.sleep)


if __name__ == '__main__':
    main() 
