import datetime
import os
import sys
import time

import support


ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('protocols', 1)[0]


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


def print_content(data:list, dbms:str, table:str=None):
    """
    Print data to screen
    :args:
        data - either a list or dict of data sets
        dbms:str - logical database name
        table:str - table name, if data is dict use keys as table name(s)
    """
    if isinstance(data, list):
        for row in data:
            row['dbms'] = dbms
            row['table'] = table
            print(support.json_dumps(row))
    elif isinstance(data, dict):
        for table in data:
            for row in data[table]:
                row['dbms'] = dbms
                row['table'] = table
                print(support.json_dumps(row))



def write_to_file(data:list, dbms:str, table:str, timestamp:str=None, data_dir:str=os.path.join(ROOT_PATH, 'data'),
                  compress:bool=False, exception:bool=False)->(bool, str):
    """
    Write content to file + compress if True
    :args:
        data - either a list or dict of data sets
        dbms:str - logical database name
        table:str - table name, if data is dict use keys as table name(s)
        timestamp:str - timestamp value to use for file name
        data_dir:str - directory to store content in
        compress:bool - whether or not to compress generated file(s)
        exception:bool - whether to print error messages or not
    :params:
        status:bool
        timestamp:str - file timestamp value (for name)
        full_path:str - file path
    """
    status = True
    if timestamp is None:
        full_path = os.path.join(data_dir, f'{dbms}.{table}.0.{str(int(time.time()))}.json')
    else:
        full_path = os.path.join(data_dir, f'{dbms}.{table}.0.{timestamp}.json')

    if not os.path.isdir(data_dir):
        try:
            os.makedirs(data_dir)
        except Exception as error:
            if exception is True:
                print(f'Failed to create directory: {full_path} (Error: {error})')
            status = False

    if status is True:
        try:
            with open(full_path, 'w') as f:
                try:
                    f.write(data)
                except Exception as error:
                    if exception is True:
                        print(f'Failed to write content into {full_path} (Error: {error}')
                    status = False
        except Exception as error:
            if exception is True:
                print(f'Failed to open file {full_path} in order to write data (Error: {error})')
            status = False
        else:
            if compress is True:
                status = support.compress(input_file=full_path, exception=exception)

    return status, full_path



# def write_to_file(data:list, dbms:str, table:str=None, data_dir:str=os.path.join(ROOT_PATH, 'data'),
#                   compress:bool=False, exception:bool=False)->bool:
#     """
#     Write content to file
#     :args:
#         data - either a list or dict of data sets
#         dbms:str - logical database name
#         table:str - table name, if data is dict use keys as table name(s)
#         data_dir:str - directory to store content in
#         compress:bool - whether or not to compress generated file(s)
#         exception:bool - whether to print error messages or not
#     :params:
#         status:bool
#         timestamp:int - unique value for fil ename e
#         file_name:str - file name
#         file_path:str - full path
#     :return:
#         status
#     """
#     status = True
#     if not os.path.isdir(data_dir):
#         os.makedirs(data_dir)
#
#     if isinstance(data, list):
#         try:
#             timestamp = __timestamp_to_fn(data[0]['timestamp'])
#         except Exception as error:
#             timestamp = str(int(time.time()))
#         file_name = '%s.%s.0.%s.json' % (dbms, table, timestamp)
#         file_path = os.path.join(data_dir, file_name)
#         try:
#             with open(file_path, 'w') as f:
#                 for row in data:
#                     try:
#                         f.write(support.json_dumps(row) + '\n')
#                     except Exception as e:
#                         if exception is True:
#                             print("Failed to write line to file '%s' (Error: %s)" % (file_path, e))
#                         status = False
#         except Exception as e:
#             if exception is True:
#                 print("Failed to open file '%s' (Error: %s)" % (file_path, e))
#             status = False
#         else:
#             if compress is True:
#                 status = support.compress(input_file=file_path, exception=exception)
#
#     elif isinstance(data, dict):
#         for table in data:
#             sub_data = data[table]
#             try:
#                 timestamp = __timestamp_to_fn(data[0]['timestamp'])
#             except Exception as error:
#                 timestamp = str(int(time.time()))
#
#             file_name = '%s.%s.0.%s.json' % (dbms, table, timestamp)
#             file_path = os.path.join(data_dir, file_name)
#             try:
#                 with open(file_path, 'w') as f:
#                     for row in sub_data:
#                         try:
#                             f.write(support.json_dumps(row) + '\n')
#                         except Exception as e:
#                             if exception is True:
#                                 print("Failed to write line to file '%s' (Error: %s)" % (file_path, e))
#                             status = False
#             except Exception as e:
#                 if exception is True:
#                     print("Failed to open file '%s' (Error: %s)" % (file_path, e))
#                 status = False
#             else:
#                 if compress is True:
#                     status = support.compress(input_file=file_path, exception=exception)
#
#     return status
