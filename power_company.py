import datetime
import json
import random
import string

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


def data_generator():
    """
    Generate JSON for tables in DATA
    :params:
        table:str - Table to query
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
    table = random.choice(list(DATA))
    payloads = {}
    payload = {
        'dbms': 'afg',
        'table': table,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    }
    if table == 'synchrophasor':
        payload['source'] = int(__calculate_value(DATA[table]['source']))
        sequence = 1
        if random.choice(range(1, 10)) % 3 == 0:
            sequence = 3
        for i in range(sequence):
            synchrophasor_values = __synchrophasor_data()
            payload = {**payload, **synchrophasor_values, 'sequence': i+1}
            payloads[i] = json.dumps(payload)
    else:
        payloads = {**payload, 'value': __calculate_value(DATA[table])}
        payloads = json.dumps(payloads)

    return payloads


if __name__ == '__main__':
    for i in range(10):
        output = data_generator()
        if isinstance(output, dict):
            for indx in output:
                print(output[indx])
        else:
            print(output)




