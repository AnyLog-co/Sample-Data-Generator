import json 
 
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

