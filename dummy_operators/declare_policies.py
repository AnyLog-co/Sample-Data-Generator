import argparse
import json
import os
import requests
import yaml


def __read_yaml(yaml_file:str):
    full_path = os.path.expanduser(os.path.expandvars(yaml_file))
    if not os.path.isfile(full_path):
        print("Failed to locate YAML file,  cannot continue...")
        exit(1)
    with open(full_path) as f:
        return yaml.safe_load(f)


def __write_yaml(yaml_file:str, data:dict):
    full_path = os.path.expanduser(os.path.expandvars(yaml_file))
    if not os.path.isfile(full_path):
        print("Failed to locate YAML file,  cannot continue...")
        exit(1)
    open(full_path, 'w').close()
    with open(full_path, 'a') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def __check_policy(conn:str, policy_name:str):
    try:
        r = requests.get(url=f"http://{conn}", headers={
            "command": f"blockchain get * where name={policy_name}",
            "User-Agent": "AnyLog/1.23"
        })
    except Exception as error:
        print(f"Failed to get policy from {conn} (Error: {error})")
        exit(1)
    else:
        if not 200 <= int(r.status_code) <= 299:
            print(f"Failed to get policy from {conn} (Network Error: {r.status_code}")
            exit(1)
    return r.json()


def create_policy(policy_type:str, policy_name:str=None, parent_policy:str=None, member_id:int=None, operator_ip:str=None,
                  operator_port:int=32148)->str:
    if policy_type == 'cluster' and not parent_policy:
        policy = {
            "cluster": {
                "company": "Dummy Operators",
                "name": policy_name
            }
        }
    elif policy_type == 'cluster':
        policy = {
            "cluster": {
                "parent": parent_policy,
                "name": policy_name,
                "company": "Dummy Operators",
                "table": [{
                    "dbms": "dummy_operators",
                    "name": "dummy_data",
                    "status": "active"
                }]
            }
        }
    elif policy_type == 'operator':
        policy = {
            "operator": {
                "name": policy_name,
                "company": "Dummy Operators",
                "ip": operator_ip,
                "port": operator_port,
                "cluster": parent_policy,
                "member": member_id
            }
        }
    elif policy_type == 'table':
        policy = {
            "table": {
                "name": "dummy_data",
                "dbms": "dummy_operators",
                "create": "CREATE TABLE dummy_data (row_id SERIAL PRIMARY KEY,  insert_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),  tsd_name CHAR(3),  tsd_id INT, cpu_percent FLOAT,dbms VARCHAR(255),disk_read BIGINT,disk_space FLOAT,disk_write BIGINT,load_avg_15min FLOAT,load_avg_5min FLOAT,node_id INT,packets_recv BIGINT,packets_sent BIGINT,swap_memory INT,timestamp TIMESTAMP,uptime VARCHAR(255),virtual_memory FLOAT,PRIMARY KEY (timestamp));CREATE INDEX dummy_data_timestamp_index ON dummy_data(timestamp); CREATE INDEX dummy_data_tsd_index ON dummy_data(tsd_name, tsd_id); CREATE INDEX dummy_data_insert_timestamp_index ON dummy_data(insert_timestamp);"
            }
        }

    return policy


def __publish_policy(conn:str, ledger_conn:str, policy:dict, auth:tuple=(), timeout:int=30)->bool:
    """
    Publish policy into a network via REST POST
    :args:
        conn:str - REST connection information
        ledger_conn:str - master node or blockchain ledger connection infromation
        policy_id:dict - policy to publish
        auth:tuple - rest authentication
        timeout:str - REST timeout
    """
    status = True

    headers = {
        'command': 'blockchain push !new_policy',
        'User-Agent': 'AnyLog/1.23',
        'destination': ledger_conn
    }

    if isinstance(policy, dict):  # convert policy to str if dict
        policy = json.dumps(policy)
    raw_policy = "<new_policy=%s>" % policy

    try:
        r = requests.post(url='http://%s' % conn, headers=headers, data=raw_policy, auth=auth, timeout=timeout)
    except Exception as e:
        print('Failed to POST policy against %s (Error; %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            print('Failed to POST policy against %s (Network Error: %s)' % (conn, r.status_code))
            status = False

    return status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file', type=str, default='$HOME/Sample-Data-Generator/dummy_operators/dummy_configs.yaml', help='YAML operaator(s) config file')
    parser.add_argument('--query-node', type=str, default='127.0.0.1:32349',help='Query Node REST conn')
    parser.add_argument('--ledger-conn', type=str, default='127.0.0.1:32048', help='Ledger connection information')
    args = parser.parse_args()
    
    setup_info = __read_yaml(args.yaml_file)
    member_id = 1

    # for cluster in setup_info:
    #     output = __check_policy(conn=args.query_node, policy_name=cluster)
    #     while not output:
    #         cluster_policy = create_policy(policy_type="cluster", policy_name=cluster)
    #         __publish_policy(conn=args.query_node, policy=cluster_policy, ledger_conn=args.ledger_conn)
    #         output = __check_policy(conn=args.query_node, policy_name=cluster)
    #     cluster_policy_id = output[0]['cluster']['id']
    #     for operator in setup_info[cluster]:
    #         operator_node = f'{cluster}-{operator}'
    #         output = __check_policy(conn=args.query_node, policy_name=operator_node)
    #         old_member_id = member_id
    #         if 'member' in setup_info[cluster][operator]:
    #             member_id = setup_info[cluster][operator]
    #         while not output:
    #             operator_policy = create_policy(policy_type='operator',policy_name=operator_node,
    #                                             parent_policy=cluster_policy_id, member_id=member_id,
    #                                             operator_ip=setup_info[cluster][operator]['ip'],
    #                                             operator_port=int(setup_info[cluster][operator]['port']))
    #             __publish_policy(conn=args.query_node, policy=operator_policy, ledger_conn=args.ledger_conn)
    #             output = __check_policy(conn=args.query_node, policy_name=operator_node)
    #             if output:
    #                 if 'member' not in setup_info[cluster][operator]:
    #                     setup_info[cluster][operator]['member'] = member_id
    #                 member_id = old_member_id + 1
    #     output = __check_policy(conn=args.query_node, policy_name=cluster)
    #     while len(output) != 2:
    #         cluster_policy = create_policy(policy_type="cluster", parent_policy=cluster_policy_id, policy_name=cluster)
    #         __publish_policy(conn=args.query_node, policy=cluster_policy, ledger_conn=args.ledger_conn)
    #         output = __check_policy(conn=args.query_node, policy_name=cluster)
    #     output = __check_policy(conn=args.query_node, policy_name='dummy_data')
    #     while not output:
    #         table_policy = create_policy(policy_type="table")
    #         __publish_policy(conn=args.query_node, policy=table_policy, ledger_conn=args.ledger_conn)
    #         output = __check_policy(conn=args.query_node, policy_name='dummy_data')

    __write_yaml(yaml_file=args.yaml_file, data=setup_info)


if __name__ == '__main__':
    main()
