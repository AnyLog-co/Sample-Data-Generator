"""
MQTT Call:
run mqtt client where broker="driver.cloudmqtt.com" and port=18975 and user=mqwdtklv and password=uRimssLO4dIo and log=false and topic=(name=traffic and dbms="bring [dbms]" and table="bring [table]" and column.timestamp.timestamp="bring [timestamp]" and column.city.str="bring [city]" and column.loc.str="bring [loc]" and column.frc.str="bring [frc]" and column.current_speed.float="bring [current_speed]" and column.road_status.str="bring [road_status]")
"""
import requests
import os
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('data_generators', 1)[0]
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, PROTOCOLS)
from support import generate_timestamp

LOCATIONS = {
    'San Jose': (37.373653, -121.927853),
    'Sunnyvale': (37.400459, -122.035324),
    'Mountain View': (37.412276, -122.078734),
    'East Palo Alto': (37.468270, -122.154020),
    'Redwood City': (37.412351, -122.078709),
    'San Mateo': (37.553155, -122.296045),
    'SFO': (37.615652, -122.397504),
    'San Francisco': (37.705860, -122.394284)
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

def generate_traffic_data(api_key:str, exception:bool=False)->list:
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
    timestamp = generate_timestamp(timezone='UTC', enable_timezone_range=False)
    for city in LOCATIONS:
        url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point={LOCATIONS[city][0]}%2C{LOCATIONS[city][1]}&unit=MPH&openLr=false&key={api_key}'
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
                    'loc': f'{LOCATIONS[city][0]}, {LOCATIONS[city][1]}',
                    'frc': content['flowSegmentData']['frc'],
                    'current_speed': content['flowSegmentData']['currentSpeed'],
                    'confidence': content['flowSegmentData']['confidence']
                }

                if content['flowSegmentData']['roadClosure'] is True:
                    data['road_status'] = 'closed'
                else:
                    data['road_status'] = 'open'
                data_sets.append(data)
            else:
                if exception is True:
                    if status_code in ERROR_CODES:
                        print(f'Failed to execute GET against TomTom ({ERROR_CODES[status_code]})')
                    else:
                        print(f'Failed to execute GET against TomTom for an unknown reason')

    return data_sets

