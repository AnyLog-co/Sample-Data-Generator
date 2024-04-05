import random
from data_generator.support import create_timestamp

PING_DATA = {
    'ADVA FSP3000R7': {
        'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H',
        'min_value': 0,
        'max_value': 4
    },
    'Ubiquiti OLT': {
        'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw',
        'min_value': 0,
        'max_value': 49
    },
    'VM Lit SL NMS': {
        'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H',
        'min_value': 0,
        'max_value': 11
    },
    'Catalyst 3500XL': {
        'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw',
        'min_value': 0,
        'max_value': 49
    },
    'GOOGLE_PING': {
        'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H',
        'min_value': 2,
        'max_value': 37
    },
}

PERCENTAGECPU_DATA = {
    'ADVA FSP3000R7': {
        'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H',
    },
    'Ubiquiti OLT': {
        'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw',
    },
    'VM Lit SL NMS': {
        'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H',
    },
    'Catalyst 3500XL': {
        'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw',
    },
    'GOOGLE_PING': {
        'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba',
        'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H',
    },
}

def percentagecpu_sensor(db_name:str)->dict:
    """
    Generate Percentage CPU sensor information - data is based on information shared by Lit San Leandro
    :args:
        db_name:str - logical database name
    :params:
        device_name:str - device name to insert data for
        payload:dict - dictionary object to store
    :return:
        payload
    :sample-data:
        {
            "dbms": "test",
            "table": "percentagecpu_sensor",
            "device_name": "Catalyst 3500XL",
            "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba",
            "timestamp": "2020-12-08 02:20:11.024002",
            "value": 15.2,
            "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVR"
        }
    """
    device_name = random.choice(list(PERCENTAGECPU_DATA.keys()))
    payload = {
        'dbms': db_name,
        'table': 'percentagecpu_sensor',
        'timestamp': create_timestamp(),
        'device_name': device_name,
        'parentelement': PERCENTAGECPU_DATA[device_name]['parentelement'],
        'webid': PERCENTAGECPU_DATA[device_name]['webid'],
        'value': round(random.random() * 100, 2)
    }
    return payload


def ping_sensor(db_name:str)->dict:
    """
    Generate Ping CPU sensor information - data is based on information shared by Lit San Leandro
    :args:
        db_name:str - logical database name
    :params:
        device_name:str - device name to insert data for
        value:float - calculation for value to be stored in payload
        payload:dict - dictionary object to store
    :return:
        payload
    :sample-data:
        {
            "dbms": "test",
            "table": "percentagecpu_sensor",
            "device_name": "Catalyst 3500XL",
            "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba",
            "timestamp": "2020-12-08 02:20:11.024002",
            "value": 15.2,
            "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVR"
        }
    """
    device_name = random.choice(list(PING_DATA.keys()))
    sub_value = random.choice(range(PING_DATA[device_name]['min_value'], PING_DATA[device_name]['max_value']))
    rand_val = random.random()
    if PING_DATA[device_name]['min_value'] <= sub_value + rand_val <= PING_DATA[device_name]['max_value']:
        value = round(sub_value + rand_val, 2)
    elif PING_DATA[device_name]['min_value'] <= sub_value - rand_val <= PING_DATA[device_name]['max_value']:
        value = round(sub_value - rand_val, 2)
    elif PING_DATA[device_name]['min_value'] <= rand_val - sub_value <= PING_DATA[device_name]['max_value']:
        value = rand_val - sub_value
    else:
        value = sub_value

    payload = {
        'dbms': db_name,
        'table': 'ping_sensor',
        'timestamp': create_timestamp(),
        'device_name': device_name,
        'parentelement': PING_DATA[device_name]['parentelement'],
        'webid': PING_DATA[device_name]['webid'],
        'value': value
    }

    return payload


