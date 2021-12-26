import datetime
import os
import sys
import support


ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('protocols', 1)[0]
DATA_DIR = os.path.join(ROOT_PATH, 'data')

def __timestamp_to_fn(orig_timestamp:str)->str:
    if '+' in orig_timestamp:
        timestamp = int(datetime.datetime.strptime(orig_timestamp.split('+')[0], '%Y-%m-%d %H:%M:%S.%f').timestamp())
    elif orig_timestamp.count('-') > 2:
        timestamp = int(datetime.datetime.strptime(orig_timestamp.rsplit('-', 1)[0], '%Y-%m-%d %H:%M:%S.%f').timestamp())
    elif ' ' in orig_timestamp:
        timestamp = int(datetime.datetime.strptime(orig_timestamp, '%Y-%m-%d %H:%M:%S.%f').timestamp())
    else:
        timestamp = int(datetime.datetime.strptime(orig_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())

    return timestamp

def write_to_file(data:list, dbms:str, table:str=None)->str:
    """
    Write content to file
    :args:
        data - either a list or dict of data sets
        dbms:str - logical database name
        table:str - table name, if data is dict use keys as table name(s)
    :params:
        timestamp:int - unique value for fil ename e
        file_name:str - file name
        file_path:str - full path
    :return:
        file_path
    """
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)


    if isinstance(data, list):
        timestamp = __timestamp_to_fn(data[0]['timestamp'])
        file_name = '%s.%s.0.%s.json' % (dbms, table, timestamp)
        file_path = os.path.join(DATA_DIR, file_name)
        with open(file_path, 'w') as f:
            for row in data:
                f.write(support.json_dumps(row) + '\n')
    elif isinstance(data, dict):
        for table in data:
            sub_data = data[table]
            timestamp = __timestamp_to_fn(sub_data[0]['timestamp'])
            file_name = '%s.%s.0.%s.json' % (dbms, table, timestamp)
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, 'w') as f:
                for row in sub_data:
                    f.write(support.json_dumps(row) + '\n')

    return file_path