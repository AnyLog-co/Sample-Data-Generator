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

def write_data(device_id, header:dict , payloads:list, prep:str, watch:str):
    """
    Write paylaods to file
    :args: 
       header:dict - header information 
       payloads:list - list of payloads 
       prep:str - directory to prep the data in
       watch:dir - directory for data ready to be sent into AnyLog. if None ignored
    :param: 
       dbms:str -  database name 
       table:str - table name 
       file_name:str - file name
    :print:
       file_name 
    #  [dbms name].[table name].[data source].[hash value].[instructions].json
    """
    prep = os.path.expandvars(os.path.expanduser(prep))
    prep_file_name = '%s/%s.%s.%s.0.0.json' % (prep, header['dbms'], header['table'], device_id) 

    if watch is not None: 
       watch = os.path.expandvars(os.path.expanduser(watch))
       watch_file_name = '%s/%s.%s.%s.0.0.json' % (watch, header['dbms'], header['table'], device_id) 

    open(file_name, 'w').close() 
    for payload in payloads:
       json_payload = json.dumps(payload) 
       with open(file_name, 'a') as f: 
          f.write('%s\n' % json_payload) 

    if watch is not None: 
      os.rename(prep_file_name, watch_file_name)
      print('Data located in: %s' % watch_file_name) 
   else:
      print('Data located in: %s' % prep_file_name) 

