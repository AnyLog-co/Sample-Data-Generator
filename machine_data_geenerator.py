import argparse
import json
import random
import requests
import socket
import uuid
import time

def __extract_conn(conn_info:str)->(str, tuple):
    conns = {}
    for conn in conn_info.split(","):
        auth = ()
        if '@' in conn:
            auth, conn = conn.split('@')
            auth = tuple(auth.split(':'))
        conns[conn] = auth
    return conns

def __publish_data(publisher:str, conn:str, payload:list, topic:str, qos:int=0, auth:tuple=(), timeout:float=30,
                   exception:bool=False):
    if publisher == 'post':
        from data_publisher.publisher_rest import publish_via_post
        publish_via_post(conn=conn, payload=payload, topic=topic, auth=auth, timeout=timeout, exception=exception)
    elif publisher == 'mqtt':
        from data_publisher.publisher_mqtt import publish_mqtt
        publish_mqtt(conn=conn, payload=payload, topic=topic, qos=qos, auth=auth, exception=exception)
    elif publisher == 'kafka':
        from data_publisher.publisher_kafka import publish_kafka
        publish_kafka(conn=conn, payload=payload, topic=topic, auth=auth, exception=exception)
    elif publisher == 'print':
        print(json.dumps(payload, indent=4))


def generate_id()->str:
    """
    Generate a unique ID for the data based on IP address - used as device name
    :params:
        local_ip:str - internal IP of the machine / device
        unique_value:uuid - generated UUID based on namespace and local_ip
    :returnn:
        uniquee_value as string
    """
    try:
        # Connect to an external server to get the correct local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
    except Exception as e:
        raise Exception(f"Error: {e}")

    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    unique_value = uuid.uuid5(namespace, local_ip)
    return unique_value.__str__()


def create_blockchain_policy(device_id:str):
    """
    Generate policy for r_50 device
    :args:
        device_id:str - device ID (from generate_id())
    :params:
        costco_locations:list - list of costco locations
       costco:int - selected costco from list
       new_policy:dict - generated policy
    :return:
        new_policy as string
    :sample policy:
    {
        "r_50": {
            "device_id": "e4a5580c-741e-5826-aa63-9804e39af622",
            "company": "Orics",
            "loc": "41.8314, -87.655",
            "city": "Chicago",
            "state": "IL"
        }
    }
    """
    costco_locations = [
        {"lat": 37.7752, "long": -122.4193, "state": "CA", "city": "San Francisco"}, # 450 10th St, San Francisco, CA 94103
        {"lat": 47.6800, "long": -122.2001, "state": "WA", "city": "Kirkland"},  # 8629 120th Ave NE, Kirkland, WA 98033
        {"lat": 32.9225, "long": -96.7678, "state": "TX", "city": "Dallas"},  # 8055 Churchill Way, Dallas, TX 75251
        {"lat": 41.8314, "long": -87.6550, "state": "IL", "city": "Chicago"},  # 1430 S Ashland Ave, Chicago, IL 60608
        {"lat": 40.8011, "long": -73.9335, "state": "NY", "city": "New York"},  # 517 E 117th St, New York, NY 10035
        {"lat": 25.7596, "long": -80.3050, "state": "FL", "city": "Miami"},  # 7795 W Flagler St #01, Miami, FL 33144
        {"lat": 45.5597, "long": -122.5443, "state": "OR", "city": "Portland"},  # 4849 NE 138th Ave, Portland, OR 97230
        {"lat": 43.5821, "long": -116.2235, "state": "ID", "city": "Boise"},  # 2051 S Cole Rd, Boise, ID 83709
        {"lat": 34.1254, "long": -118.2844, "state": "CA", "city": "Los Angeles"} # 2901 Los Feliz Blvd, Los Angeles, CA 90039
    ]

    costco = random.randint(0, len(costco_locations)-1)
    new_policy = {
        "r_50": {
            "device_id": device_id,
            "company": "Orics",
            "loc": f"{costco_locations[costco]['lat']}, {costco_locations[costco]['long']}",
            "city": costco_locations[costco]['city'],
            "state": costco_locations[costco]['state']
        }
    }
    return new_policy


def publish_policy(conn:str, device_id:str):
    """
    Based on r_50 policy name (generate_id()), decide whether to publish policy or not.
    publish policy if DNE
    :args:
        conn:str - REST connection infromation
        device_id:str - policy ID (generate_id())
    :params:
        response:requests.GET / requests.POST
        output:list - blockchain GET result
        policy:dict - generated policy
        new_policy:str - serialized policy


    """
    # check if device already exists
    try:
        response = requests.get(url=f'http://172.105.86.168:32149',
                                headers={'command': f'blockchain get r_50 where device_id = {device_id}',
                                         'User-Agent': 'AnyLog/1.23'})
    except requests.exceptions.ConnectionError as error:
        raise requests.exceptions.ConnectionError(f'Failed to get data from {conn} (Error: {error})')
    except requests.exceptions.Timeout as error:
        raise requests.exceptions.Timeout(f'Failed to get data from {conn} (Error: {error})')
    except requests.exceptions.RequestException as error:
        raise requests.exceptions.RequestException(f'Failed to get data from {conn} (Error: {error})')
    except Exception as error:
        raise Exception(f'Failed to get data from {conn} (Error: {error})')
    else:
        if not 200 <= int(response.status_code) < 300:
            raise requests.exceptions.ConnectionError(f'Failed to get data from {conn} (Network Error: {response.status_code})')
        try:
            output = response.json()
        except requests.exceptions.JSONDecodeError as error:
            raise requests.exceptions.JSONDecodeError(f'Failed to get data from {conn} (Error: {error})')
        except requests.exceptions.InvalidJSONError as error:
            raise requests.exceptions.InvalidJSONError(f'Failed to get data from {conn} (Error: {error})')
        except Exception as error:
            raise Exception(f'Failed to get data from {conn} (Error: {error})')

    if not output: # declare new device if DNE
        policy = create_blockchain_policy(device_id=device_id)
        new_policy = f"<new_policy={json.dumps(policy)}>"
        try:
            response = requests.post(url=f'http://{conn}', headers={'command': 'blockchain insert where policy=!new_policy and local=true and master=!ledger_conn',
                                                                    'User-Agent': 'AnyLog/1.23'}, data=new_policy)
        except requests.exceptions.ConnectionError as error:
            raise requests.exceptions.ConnectionError(f'Failed to POST data to {conn} (Error: {error})')
        except requests.exceptions.Timeout as error:
            raise requests.exceptions.Timeout(f'Failed to POST data to {conn} (Error: {error})')
        except requests.exceptions.RequestException as error:
            raise requests.exceptions.RequestException(f'Failed to POST data to {conn} (Error: {error})')
        except Exception as error:
            raise Exception(f'Failed to POST data to {conn} (Error: {error})')
        else:
            if not 200 <= int(response.status_code) < 300:
                raise requests.exceptions.ConnectionError(f'Failed to POST data to {conn} (Network Error: {response.status_code})')


def get_data():
    """
    Pull data from Modbus server
    :params:
        response:requests.GET
    :return:
        success - JSON data
        else - raise exception
    """
    try:
        response = requests.get(url='http://127.0.0.1:8481/simulated_data')
    except requests.exceptions.ConnectionError as error:
        raise requests.exceptions.ConnectionError(f'Failed to get data from service (Error: {error})')
    except requests.exceptions.Timeout as error:
        raise requests.exceptions.Timeout(f'Failed to get data from service (Error: {error})')
    except requests.exceptions.RequestException as error:
        raise requests.exceptions.RequestException(f'Failed to get data from service (Error: {error})')
    except Exception as error:
        raise Exception(f'Failed to get data from service (Error: {error})')
    else:
        if not 200 <= int(response.status_code) < 300:
            raise requests.exceptions.ConnectionError(f'Failed to get data from service (Network Error: {response.status_code})')
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as error:
            raise requests.exceptions.JSONDecodeError(f'Failed to get data from service (Error: {error})')
        except requests.exceptions.InvalidJSONError as error:
            raise requests.exceptions.InvalidJSONError(f'Failed to get data from service (Error: {error})')
        except Exception as error:
            raise Exception(f'Failed to get data from service (Error: {error})')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default='127.0.0.1:32149',
                        help='connection information (example: [user]:[passwd]@[ip]:[port])')
    parser.add_argument('publisher', type=str, default='print',
                        choices=['post', 'mqtt', 'print'], help='format to publish data')
    parser.add_argument('--batch-size', type=int, default=10, help='number of rows per insert batch')
    parser.add_argument('--total-rows', type=int, default=10,
                        help='total rows to insert - if set to 0 then run continuously')
    parser.add_argument('--sleep', type=float, default=0.5, help='wait time between each row to insert')
    parser.add_argument('--db-name', type=str, default='test', help='logical database name')
    parser.add_argument('--topic', type=str, default='anylog-demo', help='topic name for POST, MQTT and Kafka')
    parser.add_argument('--timeout', type=float, default=30, help='REST timeout')
    parser.add_argument('--qos', type=int, choices=list(range(0, 4)), default=0, help='Quality of Service')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='Whether to print exceptions')
    args = parser.parse_args()

    total_rows = 0
    conns = __extract_conn(conn_info=args.conn)
    payloads = []
    device_id = generate_id()  # get policy ID (used as name)
    publish_policy(conn=args.conn, device_id=device_id)

    while True:
        conn = random.choice(list(conns.keys()))
        auth = conns[conn]

        payload = get_data()
        if payload and isinstance(payload, dict):
            payload['serial_number'] = device_id
            payloads.append({'d': payload})

        if len(payloads) == args.batch_size or (args.total_rows <= len(payloads) + total_rows and args.total_rows != 0):
            __publish_data(publisher=args.publisher, conn=conn, payload=payloads, topic=args.topic, qos=args.qos,
                           auth=auth, timeout=args.timeout, exception=args.exception)
            total_rows += len(payloads)
            payloads = []

        if total_rows >= args.total_rows:
            exit(1)
        time.sleep(args.sleep)



if __name__ == '__main__':
    main()
    # print(create_blockchain_policy())



