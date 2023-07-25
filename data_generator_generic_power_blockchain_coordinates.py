import argparse
import json
import re
import requests


LOCATIONS = {
    'Los Angeles, CA': '33.8121, -117.91899',
    'San Francisco, CA': '37.786163522, -122.404498382',
    'Seattle, WA': '47.620182, -122.34933',
    'Philadelphia, PN': '39.949566, -75.15026',
    'Arlington, VA': '38.870983,  -77.05598',
    'Washington DC': '38.89773, -77.03653',
    'New York City, NY': '40.758595, -73.98447',
    'Orlando, FL': '28.37128, -81.51216',
    'Houston, TX': '29.97980499267578, -95.56627655029297',
    'Las Vegas': '36.1147, -115.1728'
}


def __validate_pattern(conn:str)->dict:
    """
    validate connection pattern, if not error then split to connection + authentication
    :args:
        conn:str - user inputted pattern
    :params:
        pattern1:str - 127.0.0.1:32048
        pattern1:str - user:password@127.0.0.1:32048
        connections:dict - connection dict
    :return:
        connections
    """
    pattern1 = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')
    pattern2 = re.compile(r'^\w+:\w+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')

    if not pattern1.match(conn) and not pattern2.match(conn):
        raise argparse.ArgumentTypeError(
            f'Invalid connection format: {conn}. Supported formats: 127.0.0.1:32049 or user:passwd@127.0.0.1:32049')
    else:
        connections = {}
        ip_port = conn.split("@")[-1]
        connections[ip_port] = None
        if '@' in conn:
            connections[ip_port] = tuple(list(conn.split('@')[0].split(':')))

    return connections

def __publish_coordinates(conn:str, ledger_conn:str, policy:str, auth:tuple=(), timeout:int=30, exception:bool=False)->(bool, str):
    """
    Publish coordinates to blockchain via REST
    :args:
        conn:str - REST connection information
        ledger_conn:str - master node / blockchain connection information
        policy:str - content to publish
        auth:str - REST authentication
        timeout:int - REST timeout
        exception:bool - exception
    :params:
        status:bool
        headers:dict - REST header information
        error:str - error message
        r:requests.post - request post
    :return:
        status, error
    """
    error = None
    status = True
    headers = {
        'command': 'blockchain push !new_policy',
        'User-Agent': 'AnyLog/1.23',
        'destination': ledger_conn
    }

    try:
        r = requests.post(url=f'http://{conn}', headers=headers, data=policy, auth=auth, timeout=timeout)
    except Exception as error:
        status = False
        if exception is True:
            error  = error
    else:
        if int(r.status_code) != 200:
            status = False
            if exception is True:
                error = int(r.status_code)

    return status, error


def main():
    """
    The following adds policies to the blockchain associated the data coming from POWER data generator
    :positional arguments:
        rest_conn             REST connection information
        ledger_conn           TCP master information
    :options:
        -h, --help                          show this help message and exit
        -t, --timeout       TIMEOUT         REST timeout period (default: 30)
        -e, --exception     [EXCEPTION]     whether to print exceptions (default: False)
    :global:
        LOCATIONS:dict - locations
    :params:
        status:bool
        policy:dict - generated policy(s) stored on blockchain
        str_policy:str - JSON of dict
        conn:str - REST connection information
        auth:tuple - authentication for REST
        error:str - error message

    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('rest_conn',       type=__validate_pattern,   default='127.0.0.1:2049', help='REST connection information')
    parser.add_argument('ledger_conn',     type=__validate_pattern,   default='127.0.0.1:2048', help='TCP master information')
    parser.add_argument('-t', '--timeout', type=int, default=30, help='REST timeout period')
    parser.add_argument('-e', '--exception',  type=bool, nargs='?', const=True, default=False, help='whether to print exceptions')
    args = parser.parse_args()

    policy = {'panel': {
        'name': "",
        'city': "",
        'loc': "",
        'owner': 'AFG'
    }}

    conn = list(args.rest_conn)[0]
    auth = args.rest_conn[conn]
    error = None

    for location in LOCATIONS:
        policy['panel']['name'] = 'Panel %s' % str(int(list(LOCATIONS).index(location)) + 1)
        policy['panel']['city'] = location
        policy['panel']['loc'] = LOCATIONS[location]

        try:
            str_policy = json.dumps(policy)
        except Exception as error:
            if args.exception is True:
                print(f"Failed to convert policy from dictionary to string - Location: {location} (Error: {error})")
            exit(1)

        status, error = __publish_coordinates(conn=args.rest_conn, ledger_conn=args.ledger_conn, policy=str_policy,
                                              auth=auth, timeout=args.timeout, exception=args.exception)

        if status is False and isinstance(error, int):
            print(f"Failed to insert policy for {location} in blockchain (Network Error: {error})")
        elif status is False and isinstance(error, str):
            if status is False and isinstance(error, int):
                print(f"Failed to insert policy for {location} in blockchain (Error: {error})")
        elif status is False:
            print(f"Failed to insert policy for {location} in blockchain")


if __name__ == '__main__':
    main()

