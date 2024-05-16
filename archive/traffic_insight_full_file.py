import datetime
import json
import os
import requests

LOCATIONS = {
    'San Jose': {
        'camera': '3e04896e-a28f-46f0-b481-6fe7370400a8',
        'location': (37.373653, -121.927853),
        'intersection': '101 N / 85 E',
        'server': '127.0.0.1:32159'
    },
    'San Francisco': {
        'camera': 'f5de1578-ec3c-4ea5-92f5-b6031c143b93',
        'location': (37.767880, -122.405473),
        'intersection': '101 N / 80 E',
        'server': '127.0.0.1:32149'
    }
}

ERROR_CODES = {
    400: 'Bad request: usually due to a malformed syntax.',
    403: 'Forbidden: The supplied API Key is not valid for this request',
    405: 'Method Not Allowed: The provided HTTP Request method is known by the server, but is not supported by the target resource',
    429: 'Too Many Requests: Too many requests were sent in a given amount of time for the supplied API Key',
    500: 'Internal Server Error',
    503: 'Service currently unavailable',
    596: 'Service not found: Unknown version of the service'
}

API_KEY = 'jAhhBAekAfLn8KxeWv09dUgbsWZ4XRdc'


def __put_data(conn:str, payload:dict):
    """
    Insert data via PUT command
    :args:
        conn:str - REST connection information
        payload:dict - data to upload
    :params:
        headers:dict - REST header information
    """
    headers = {
        'type': 'json',
        'dbms': 'fleet_command',
        'table': 'traffic_data',
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }
    try:
        r = requests.put('http://%s' % conn, headers=headers, data=json.dumps(payload))
    except Exception as e:
        print('Failed to send data via PUT against %s (Error: %s)' % (conn, e))
    else:
        if int(r.status_code) != 200:
            print('Failed to send data via PUT against %s due to network error: %s' % (conn, r.status_code))



def generate_traffic_data(exception:bool=False)->list:
    if os.path.isfile('data/fleet_command.traffic_data.0.json'): 
        try: 
            with open('data/fleet_command.traffic_data.0.json', 'r') as f: 
                try: 
                    for line in f.readlines(): 
                        dict_line = json.loads(line)
                        conn = LOCATIONS[dict_line['city']]['server']
                        __put_data(conn=conn, payload=dict_line)
                except Exception as e: 
                    if exception is True: 
                        print(f'Failed to read content in file (Error: {e}')
        except Exception as e: 
            if exception is True: 
                print(f'Failed to open file (Error: {e})') 

if __name__ == '__main__':
    generate_traffic_data(exception=True)
