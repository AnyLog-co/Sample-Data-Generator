import datetime
import json
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
    """
    Generate real-time traffic data from TomTom
    :apiKey:
        jAhhBAekAfLn8KxeWv09dUgbsWZ4XRdc
    :args:
        api_key:str - API key for getting data
        exception:bool - whether or not to print exceptions
    :params:
        data_set:list - content to send into AnyLog
        data:dict - generated data to store in operator(s)
        timestamp:str - generated timestamp (UTC current)
        url:str - URL to get data from
        r:requests.GET - request content
        status_code:int - request status code
    :return:
        data_sets
    """
    data_sets = []
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
    for city in LOCATIONS:
        url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point={LOCATIONS[city]["location"][0]}%2C{LOCATIONS[city]["location"][1]}&unit=MPH&openLr=false&key={API_KEY}'
        try:
            r = requests.get(url=url, headers={'accept': '*/*'})
        except Exception as e:
            print(f"Failed to execute GET against TomTom API (Error: {e})" )
        else:
            status_code = int(r.status_code)
            if status_code == 200:
                content = r.json()
                data = {
                    'timestamp': timestamp,
                    'city': city,
                    'location': f'%s, %s' % (LOCATIONS[city]['location'][0], LOCATIONS[city]['location'][1]),
                    'camera': LOCATIONS[city]['camera'],
                    'intersection': LOCATIONS[city]['intersection'],
                    'frc': content['flowSegmentData']['frc'],
                    'current_speed': content['flowSegmentData']['currentSpeed'],
                    'confidence': content['flowSegmentData']['confidence']
                }

                if content['flowSegmentData']['roadClosure'] is True:
                    data['road_status'] = 'closed'
                else:
                    data['road_status'] = 'open'
                __put_data(conn=LOCATIONS[city]['server'], payload=data)
            else:
                if exception is True:
                    if status_code in ERROR_CODES:
                        print(f'Failed to execute GET against TomTom ({ERROR_CODES[status_code]})')
                    else:
                        print(f'Failed to execute GET against TomTom for an unknown reason')


if __name__ == '__main__':
    generate_traffic_data(exception=True)