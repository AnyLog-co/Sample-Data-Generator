import json
import os 

def __convert_json(payload:dict)->str: 
    """
    Convett dict to JSON 
    :args: 
        payload:dict 
    :return: 
       paylaod converted to string 
    """
    try: 
        return json.dumps(payload)
    except Exception as e: 
        print('Failed to convert JSON') 
        return None 

def __create_dir(dir_path:str)->str: 
    """
    Expand path + validate dir exists
    :args: 
        dir_path:str - directory path 
    :return: 
        extracted dir_path 
    """
    dir_path = os.path.expanduser(os.path.expandvars(dir_path))
    if not os.path.isdir(dir_path): 
        os.makedirs(dir_path)
    return dir_path 

def print_store(payloads:list)->bool: 
    """
    Print rows to screen as JSON objects
    :args: 
        payloads:dict - payloads
    :param: 
        output:None - object to validate JSON worked 
    :return: 
        If fails to convert to json returns False 
    """
    output = None 
    for payload in payloads: 
        output = __convert_json(payload)
        if output is None: 
           return False
        print(output) 
    return True 

def file_store(payloads:list, dbms:str, table_name:str, prep_dir:str, watch_dir:str)->bool:
    """
    Store data in file 
    :args: 
        payloads:list - data to store in file 
        dbms:str - logical databse to store data in 
        table_name: - logical table name to store data in 
        prep_dir:str - dir to prep data in 
        watch_dir:str - dir ready to be stored on AnyLog 
    :param: 
        device_id:str - device id for file name 
        timestamp:str - timestamp for file 
        file_name:str - file to store data in 
    """
    prep_dir = __create_dir(prep_dir)
    watch_dir = __create_dir(watch_dir)

    try:
        device_id = payloads[0]['parentelement'].replace('-', '')
    except Exception as e: 
        device_id = 0 
    
    timestamp = payloads[0]['timestamp'].replace('-', '').replace(' ', '').replace(':', '').replace('.', '')

    file_name = '%s/%s.%s.%s.%s.json' % (prep_dir, dbms, table_name, device_id, timestamp) 
    open(file_name, 'w').close() 

    for payload in payloads: 
        output = __convert_json(payload) 
        with open(file_name, 'a',) as f: 
            f.write('%s\n' % output) 

    if watch_dir is not None: 
        os.rename(file_name, file_name.replace(prep_dir, watch_dir))
        print('Data located in %s' % file_name.replace(prep_dir, watch_dir)) 
    else: 
        print('Data located in %s' % file_name)
