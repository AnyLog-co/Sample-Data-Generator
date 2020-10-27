import datetime
import random 
import string
import uuid

PING_DATA = {
        'ADVA FSP3000R7': {
            'parentelement': str(uuid.uuid4()),
            'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H',
            'min_value': 10,
            'max_value': 40
        },
        'Ubiquiti OLT': {
            'parentelement': str(uuid.uuid4()),
            'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw',
            'min_value': 10,
            'max_value': 90
        },
        'VM Lit SL NMS': {
            'parentelement': str(uuid.uuid4()),
            'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H',
            'min_value': 10,
            'max_value': 140
        },
        'Catalyst 3500XL': {
            'parentelement': str(uuid.uuid4()),
            'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw',
            'min_value': 10,
            'max_value': 440
        },
        'GOOGLE_PING': {
            'parentelement': str(uuid.uuid4()),
            'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H',
            'min_value': 20,
            'max_value': 440
        },
        'ANYLOG_PING': {
            'parentelement': str(uuid.uuid4()),
            'webid': 'F1BbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVSTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5Y',
            'min_value': 100,
            'max_value': 1000
        }
}

def get_ping_data()->dict: 
   """
   Generate dict forr ping_data  
   :args: 
      PING_DATA:dict - dict summary of ping sensor
   :param: 
      timestamp:str
      device_name:str
      parentelement:str 
      webiid:str - str 
      min/max value:int - value range to get value from 
   :return: 
      data dict based on information generated by PING_DATA 
   """
   timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') 
   device_name = random.choice(list(PING_DATA.keys()))
   parentelement = PING_DATA[device_name]['parentelement'] 
   webid = PING_DATA[device_name]['webid'] 
   value = random.choice(range(PING_DATA[device_name]['min_value'], PING_DATA[device_name]['max_value']))

   data = {'timestamp': timestamp, 'device_name': device_name, 'parentelement': parentelement, 'webid': webid, 'value': value} 
   return data

