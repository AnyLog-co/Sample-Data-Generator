import random

LOCATIONS = [
    '33.8121, -117.91899', # LA
    '37.786163522 -122.404498382', # SF
    '47.620182, -122.34933', # Seattle
    '39.949566, -75.15026', # Phili
    '38.870983,  -77.05598', # Arlington
    '38.89773, -77.03653', # DC
    '40.758595, -73.98447', # NYC
    '28.37128, -81.51216' # Orlando 
    '29.97980499267578, -95.56627655029297', # Houston
    '36.1147, -115.1728' # Las Vegas
]

DATA = {
    'solar': [5, 50],    # Solar controller
    'battery': [5, 50],  # Battery controller
    'inverter': [5, 50], # Inverter controller
    'eswitch': [5, 50],  # Electric Switch controller
    'pmu': [5, 50],
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
        }
}


def __calculate_value(val_range:list)->float:
    """
    Calculate a random value within a given range
    :args:
        val_range:list - range between 2 values
    :params:
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
    data_set['analog'] = random.random() * random.randrange(0, 15)

    return data_set


def data_generator(db_name:str)->dict:
    """
    Generate data for non-synchorphiser table
    :args:
        db_name:str - logical database name
    :params:
        payloads:list - dictionary of data
    :return:
        payloads
    """
    payloads = []
    location = random.choice(LOCATIONS)
    for table in DATA:
        payload = {
            'dbms': db_name,
            'table': table,
            'location': location
        }
        if table != 'synchrophasor':
            payload['value'] = __calculate_value(DATA[table])
        else:
            synchrophasor_data = __synchrophasor_data()
            for key in synchrophasor_data:
                payload[key] = synchrophasor_data[key]

        payloads.append(payload)

    return payloads

