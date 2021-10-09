import argparse
import datetime
import json
import random
import string
import time

from protocols.rest_protocol import send_data

LOCATIONS = [
    'Los Angeles, CA',
    'San Francisco, CA',
    'Seattle, WA',
    'Philadelphia, PN',
    'Arlington, VA',
    'Washington, DC',
    'New York City, NY',
    'Orlando, FL',
    'Houston, TX',
    'Las Vegas, NV'
]


DATA = {
    'synchrophasor': {
        'source': [1, 6],
        'phasor': [
            'pOueAFmP',
            'bXlvzdYc',
            'OEPXqHfu',
            'qAgrrCKb',
            'IRFVtDob',
            'aUMkcaLs',
            'zmHtgsBC',
            'TNeSttkM',
            'xGbCsofo',
            'pYWfJUkv'
        ],
        'frequency': [300, 2500],
        'dfreq': [120, 1000]
    },
    'solar': [5, 50],    # Solar controller
    'battery': [5, 50],  # Battery controller
    'inverter': [5, 50], # Inverter controller
    'eswitch': [5, 50],  # Electric Switch controller
    'pmu': [5, 50]
}



def __validate_cities(user_inputy_city:str)->list:
    """
    Validate city/cities provided are in Locations
    :args:
        user_inputy_city:str - user input of city
    :params:
        status:boool
        return_value:list - value to return
    :return:
        if city/cities provided are in LOCATIONS return city as list, else return list of None
    """
    return_value = []
    if user_inputy_city is not None:
        if 'Washington DC' in user_inputy_city:
            user_inputy_city = user_inputy_city.replace('Washington DC', 'Washington, DC')

        for city in user_inputy_city.split(','):
            if user_inputy_city.split(',').index(city) % 2 == 0:
                index = user_inputy_city.split(',').index(city)
                city = '%s,%s' % (user_inputy_city.split(',')[index], user_inputy_city.split(',')[index + 1])
                city = city.lstrip()
                if city == 'Washington, DC':
                    city = city.replace(',', '')
                return_value.append(city)

        for city in return_value:
            if city not in LOCATIONS:
                return_value.pop(return_value.index(city))

    if return_value is [] or user_inputy_city is None:
        return_value = None

    return return_value


def __validate_tables(user_input_table:str)->list:
    """
    Validate table/tables provided are in DATA
    :args:
        user_input_table:str - user input of table
    :params:
        status:boool
        return_value:list - value to return
    :return:
        if table/tables provided are in DATA return city as list, else return list of None
    """
    return_value = []
    if user_input_table is not None:
        return_value = user_input_table.split(",")
        for table in return_value:
            if table not in DATA:
                return_value.remove(table)
    if user_input_table is None or return_value is None:
        return_value = None

    return return_value


def __extract_city_table(cities:list, tables=list)->(str, str):
    """
    Get city and table names
    :args:
        cities:list - list of cities
        tables:list - list of tables
    :params:
        city:str - city to use
        table:str - table to use
    :return:
        city, table
    """
    city = random.choice(LOCATIONS)
    table = random.choice(list(DATA.keys()))
    if cities is not None:
        city = random.choice(cities)
    if tables is not None:
        table = random.choice(tables)

    return city, table

def __analog_angle()->float:
    """
    Calculate change in the angle of the Sun
    """
    return random.random() * random.randrange(0, 15)

    
def __calculate_value(val_range:list)->float:
    """
    Calculate a random value within a given rangge
    :args:
        val_range:list - range between 2 values
        base_float:int - random value within val_range
        float_value:int - base_value * random.random()
    :return:
        float value within range
    """
    base_value = random.randrange(val_range[0], val_range[1])
    float_value = random.random() * base_value

    if val_range[0] < float_value + base_value < val_range[1]:
        return float_value + base_value 
    elif val_range[0] < float_value < val_range[1]:
        return float_value
    elif val_range[0] + float_value < val_range[1]:
        return val_range[0] + float_value
    elif val_range[1] - float_value < val_range[0]:
        return val_range[1] - float_value
    else:
        return float_value - random.random()


def __synchrophasor_data():
    """
    Generate values for synchrophasor data
    :params:
        data:dict - synchrophasor from DATA
        data_set:dict - values for synchrophasor
    :return:
        data_set
    """
    data = DATA['synchrophasor']
    data_set = {}

    data_set['phasor'] = random.choice(data['phasor'])
    data_set['frequency'] = __calculate_value(data['frequency'])
    data_set['dfreq'] = __calculate_value(data['frequency'])
    data_set['analog'] = __analog_angle()

    return data_set


def data_generator(db_name:str, table:str, city:str=None)->dict:
    """
    Generate JSON for tables in DATA
    :args:
        db_name:str - Database name
        table:str - table to extract data from
        city:str - Secify a specific city. If set to None each iteration will be a different city
    :params:
        table:str - Table to generate data for
        payloads:dict - payloads
        payload:dict - base payload
    :sample JSON:
        # synchrophasor
        {
            "dbms": "afg",
            "table": "synchrophasor",
            "timestamp": "2021-09-22 20:00:10.352414",
            "source": 4,
            "phasor": "zmHtgsBC",
            "frequency": 2124.3698062781855,
            "dfreq": 704.2753674876934,
            "analog": 3.2402972012617637,
            "sequence": 1
        }
        # Other
        {
            "dbms": "afg",
            "table": "pmu",
            "timestamp": "2021-09-22 20:00:10.352538",
            "value": 30.60280967105402
        }
    :return:
       JSON of payloads
    """
    payloads = {}
    payload = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        'location': city
    }

    if table == 'synchrophasor':
        payload['source'] = int(__calculate_value(DATA[table]['source']))
        sequence = 1
        if random.choice(range(1, 10)) % 3 == 0:
            sequence = 3
        for i in range(sequence):
            synchrophasor_values = __synchrophasor_data()
            payload = {**payload, **synchrophasor_values, 'sequence': i+1}
            payloads[i] = payload
    else:
        payload = {**payload, 'value': __calculate_value(DATA[table])}
        payloads[0] = payload

    return payloads


def send_put_data(conn:str, dbms:str, table:str, payloads:dict):
    """
    Send data (payloads) to AnyLog via POST
    :args:
        table:str - table in payloads
        conn:str - AnyLog REST IP & Port to send data to
        payloads:dict - results from data_generator
    """
    for indx in payloads:
        #print(payloads[indx])
        send_data(payloads=payloads[indx], conn=conn, dbms=dbms, table_name=table, mode='streaming')


def main():
    """
    Main for generating power company data
        1. Generate data
        2. POST to AnyLog - requires REST MQTT on node
    :positional arguments:
        conn    AnyLog REST IP & Port to send data to   (default: 172.104.180.110:2049)
        dbms    Database to store data in               (default: power_company)
    :optional arguments:
         -h, --help     show this help message and exit
         -t, --table    tables to get data from. If set to 'random' a different table will be selected each iteration.
            * synchrophasor
            * solar
            * battery
            * inverter
            * eswitch
            * pmu
            * random (default) - the program will selwct a different table each iteration
        -c, --city          Specify a specific city. If set to None each iteration will be a different city (default: None)
            'Los Angeles, CA',
            'San Francisco, CA',
            'Seattle, WA',
            'Philadelphia, PN',
            'Arlington, VA',
            'Washington DC',
            'New York City, NY',
            'Orlando, FL',
            'Houston, TX',
            'Las Vegas, NV'
        -i, --iteration     number of iterations. if set to 0 run continuously  (default: 0)
        -s, -sleep          wait between insert                                 (default: 0)
    :params:
        payloads:dict - results from data_generator
    :mqtt:
        run mqtt client where broker=rest and user-agent=anylog and topic=(
            name=test and dbms="bring [dbms]" and \
            table="bring [table]" and \
            column.timestamp.timestamp="bring [timestamp]" and \
            column.location.str="bring [location]" and \
            column.value.float="bring [value]" and \
            column.source.int="bring [source]" and \
            column.phasor.str="bring [phasor]" and \
            column.frequency.float="bring [frequency]" and \
            column.dfreq.float="bring [dfreq]" and \
            column.analog.float="bring [analog]" and \
            column.sequence.float="bring [sequence]"
        )

    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('conn', type=str, default='172.104.180.110:2049', help='AnyLog REST IP & Port to send data to')
    parser.add_argument('dbms', type=str, default='power_company',        help='Database to store data in')
    parser.add_argument('-t', '--table', type=str, default=None, help="Specify a specific  table get data from. If set to 'None' a different table will be selected each iteration.")
    parser.add_argument('-c', '--city',  type=str, default=None, help="Specify a specific city to get data from. If set to 'None', a different city will be selected each iteration.")
    parser.add_argument('-i', '--iteration', type=int,   default=1,        help='number of iterations. if set to 0 run continuously')
    parser.add_argument('-s', '--sleep',     type=float, default=0,        help='wait between insert')
    args = parser.parse_args()
    payloads = {}

    args.conn = args.conn.split(',')
    tables = __validate_tables(user_input_table=args.table)
    cities = __validate_cities(user_inputy_city=args.city)

    if args.iteration == 0:
        while True:
            conn = random.choice(args.conn)
            city, table = __extract_city_table(cities=cities, tables=tables)
            payloads = data_generator(db_name=args.dbms, table=table, city=city)
            send_put_data(conn=conn, dbms=args.dbms, table=table, payloads=payloads)
            time.sleep(args.sleep)

    for i in range(args.iteration):
        conn = random.choice(args.conn)
        city, table = __extract_city_table(cities=cities, tables=tables)
        payloads = data_generator(db_name=args.dbms, table=table, city=city)
        send_put_data(conn=conn, dbms=args.dbms, table=table, payloads=payloads)
        time.sleep(args.sleep)


if __name__ == '__main__':
    main()

