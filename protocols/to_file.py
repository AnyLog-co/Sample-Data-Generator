import datetime
import os
import sys
import convert_json


ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('protocols', 1)[0]
DATA_DIR = os.path.join(ROOT_PATH, 'data')


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
        timestamp = int(datetime.datetime.strptime(data[0]['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())
        file_name = '%s.%s.0.%s.json' % (dbms, table, timestamp)
        file_path = os.path.join(DATA_DIR, file_name)
        with open(file_path, 'w') as f:
            for row in data:
                f.write(convert_json.json_dumps(row) + '\n')
    elif isinstance(data, dict):
        for table in data:
            sub_data = data[table]
            timestamp = int(datetime.datetime.strptime(sub_data[0]['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())
            file_name = '%s.%s.0.%s.json' % (dbms, table, timestamp)
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, 'w') as f:
                for row in sub_data:
                    f.write(convert_json.json_dumps(row) + '\n')

    return file_path