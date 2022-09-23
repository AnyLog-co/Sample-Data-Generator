import os
import random
import sys
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('data_generators', 1)[0]
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, PROTOCOLS)
from support import generate_timestamp
    
    
DATA_SETS = {
    'fic1_pv': {'min': -160, 'max': -78}, 
    'fic1_mv': {'min': -328, 'max': 414}, 
    'fic1_sv': {'min': -357, 'max': -261}, 
    'lic1_pv': {'min': 90, 'max': 238},
    'lic1_mv': {'min': -216, 'max': 104},
    'lic1_sv': {'min': 271, 'max': 300},
    'fic2_pv': {'min': -253, 'max': -218}, 
    'fic2_mv': {'min': -165, 'max': 481}, 
    'fic2_sv': {'min': -326, 'max': 334}, 
    'lic2_pv': {'min': -355, 'max': 458}, 
    'lic2_mv': {'min': -368, 'max': 204}, 
    'lic2_sv': {'min': -235, 'max': 155}, 
    'fic3_pv': {'min': -463, 'max': -432}, 
    'fic3_mv': {'min': -397, 'max': -47}, 
    'fic3_sv': {'min': 422, 'max': 449}, 
    'lic3_pv': {'min': 22, 'max': 239}, 
    'lic3_mv': {'min': -189, 'max': -162}, 
    'lic3_sv': {'min': 345, 'max': 486}, 
    'fic4_pv': {'min': -391, 'max': 179}, 
    'fic4_mv': {'min': 208, 'max': 367}, 
    'fic4_sv': {'min': 260, 'max': 435}, 
    'lic4_pv': {'min': -497, 'max': 235}, 
    'lic4_mv': {'min': -22, 'max': 145}, 
    'lic4_sv': {'min': -462, 'max': -20}, 
    'fic5_pv': {'min': -483, 'max': -460}, 
    'fic5_mv': {'min': -237, 'max': -226}, 
    'fic5_sv': {'min': -128, 'max': 449}, 
    'lic5_pv': {'min': -231, 'max': -229}, 
    'lic5_mv': {'min': -31, 'max': 82}, 
    'lic5_sv': {'min': -326, 'max': -272}
}


def get_opcua_data(db_name:str)->dict:
    """
    Generate OPC-UA values based on data from Ai-Ops
    :args:
        db_name:str - logical database name
    :param:
        payload:dict - dict of key/values based on DATA_SETS
    :return:
        payload
    """
    payload = {
        'dbms': db_name,
        'table': 'opcua_readings'
    }
    for column in DATA_SETS:
        payload[column] = random.random() * random.choice(range(DATA_SETS[column]['min'], DATA_SETS[column]['max']))

    return  payload
