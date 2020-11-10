import json 
import os 
import requests 
import time 

def validate_connection(conn:str)->bool: 
   """
   Validate node is accessible
   :args: 
      conn:str - connection string 
   :param:
      boolean:bool - boolean status 
   :return: 
      if node is accessible return True, else return False 
   """
   boolean = False 
   try:
      r = requests.get('http://%s' % conn, headers={'type': 'info', 'details': 'get status'})
   except Exception as e: 
      print(e) 

   if 'running' in r.json()['Status']:
      boolean=True  
   return boolean 


def send_data(conn:str, header:dict, payload:dict):
   """
   Send payload to node (conn) based on header info
   :args: 
      conn:str - connection string 
      header:dict - information regarding how to store payload 
      payload:dict - data to store in database 
   :param:
      json_payload:str - payload as JSON 
   """
   json_payload = json.dumps(payload) 
   try: 
      requests.put('http://%s' % conn, headers=header, data=json_payload)
   except Exception as e:
      print(e) 
  
def print_data(payload:dict): 
   """
   Print payload to screen
   :args: 
      payload:dict - data to store in database 
   :param: 
      json_payload:str - payload as JSON 
   :print: 
      payload value 
   """
   json_payload = json.dumps(payload) 
   print(json_payload) 

def write_data(location, device_id, header:dict , payloads:list):
    """
    Write paylaods to file
    :args: 
       header:dict - header information 
       payloads:list - list of payloads 
    :param: 
       dbms:str -  database name 
       table:str - table name 
       file_name:str - file name
    :print:
       file_name 
    #  [dbms name].[table name].[data source].[hash value].[instructions].json
    """
    file_name = '%s/%s.%s.%s.0.0.json' % (location, header['dbms'], header['table'], device_id) 

    open(file_name, 'w').close() 
    for payload in payloads:
       json_payload = json.dumps(payload) 
       with open(file_name, 'a') as f: 
          f.write('%s\n' % json_payload) 

    print('Data located in: %s' % file_name) 

