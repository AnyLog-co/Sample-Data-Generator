import json 
import requests 

def validate(conn:str)->bool: 
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
   r = requests.get('http://%s' % conn, headers={'type': 'info', 'details': 'get status'})
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
  
