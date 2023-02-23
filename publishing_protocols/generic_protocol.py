import datetime
import gzip
import os

import support


ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('protocols', 1)[0]


def __write_blob(file_name:str, blob:str, exception:bool=False)->bool:
    """
    Write blob to file
    :args:
        file_name:str - file to write content  into
        blob:str - blob to write into file
        exception:bool - whether to print exceptions
    :params:
        status:bool
    :return:
        status
    """
    status = True

    try:
        with open(file_name, 'wb') as f:
            try:
                f.write(blob)
            except Exception as error:
                status = False
                if exception is True:
                    print(f"Failed to write to file {file_name} (Error: {error})")
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to open file {file_name} for data to be written (Error: {error})")

    return status


def __timestamp_to_flle_name(orig_timestamp:str)->int:
    """
    convert timestamp to integer for filename
    :args:
        orig_timestamp - timestamp to convert into integer
    :params:
        timestamp:int - converted timestamp
    :return:
        timestamp
    """
    if '+' in orig_timestamp:
        timestamp = int(datetime.datetime.strptime(orig_timestamp.split('+')[0], '%Y-%m-%d %H:%M:%S.%f').timestamp())
    elif orig_timestamp.count('-') > 2:
        timestamp = int(datetime.datetime.strptime(orig_timestamp.rsplit('-', 1)[0], '%Y-%m-%d %H:%M:%S.%f').timestamp())
    elif ' ' in orig_timestamp:
        timestamp = int(datetime.datetime.strptime(orig_timestamp, '%Y-%m-%d %H:%M:%S.%f').timestamp())
    else:
        timestamp = int(datetime.datetime.strptime(orig_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())

    return timestamp


def __write_to_file(file_path:str, payload:dict, append:bool, compress:bool, exception:bool)->bool:
    """
    Write content to file
    :args:
        file_path:str - full file path
        payload:dict - content to write
        append:bool - whether to append to file or new file
        exception:bool - whether to print exceptions
    :params:
        status:bool
        param:str - append option (a || w)
    """
    status = True
    param = 'a'
    if append is False:
        param = 'w'

    try:
        with open(file_path, param) as f:
            try:
                f.write(support.json_dumps(payload) + "\n")
            except Exception as error:
                if exception is True:
                    print(f'Failed to write line into {file_path} (Error: {error})')
                status = False
    except Exception as error:
        if exception is True:
            print(f'Failed to create file {file_path} (Error: {error})')
        status = False
    else:
        if compress is True:
            status = __zip_file(file_name=file_path, exception=exception)
            if status is True:
                try:
                    os.remove(file_path)
                except Exception as error:
                    if exception is True:
                        print(f'Failed to remove non-compressed file')

    return status

def __zip_file(file_name:str, exception:bool)->bool:
    status = True
    gzip_file_name = file_name + ".gz"
    try:
        with open(file_name, 'rb') as fn:
            try:
                data = bytearray(fn.read())
            except Exception as error:
                status = False
                if exception is True:
                    print(f'Failed to read content in {file_name} (Error: {error})')
    except Exception as error:
        status = False
        if exception is True:
            print(f'Failed to binary-read open {file_name} (Error: {error})')
    else:
        try:
            with gzip.open(gzip_file_name, 'wb') as f:
                try:
                    f.write(data)
                except Exception as error:
                    status = False
                    if exception is True:
                        print(f'Failed to write content from {file_name} into {gzip_file_name} (Error: {error})')
        except Exception as error:
            status = False
            if exception is True:
                print(f'Failed to open {gzip_file_name} for binary-write (Error: {error})')
    return status


def print_content(payloads:list):
    """
    Print data to screen
    :args:
        data - either a list or dict of data sets
        dbms:str - logical database name
        table:str - table name, if data is dict use keys as table name(s)
    """
    if isinstance(payloads, list):
        for payload in payloads:
            print(support.json_dumps(payload))
    else:
        print(support.json_dumps(payloads))


def write_to_file(payloads:list, data_dir:str=os.path.join(ROOT_PATH, 'data'), compress:bool=False,
                  exception:bool=False)->bool:
    """
    Write content to file
    :args:
        payloads:list - either a list or dict of data sets
        data_dir:str - directory to store content in
        compress:bool - whether or not to compress generated file(s) 
        exception:bool - whether to print error messages or not
    :params:
        status:bool
        timestamp:int - unique value for fil ename e
        file_name:str - file name
        file_path:str - full path
    :return:
        status
    """
    status = True
    file_list = {}

    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    for payload in payloads:
        file_name = f"{payload['dbms']}.{payload['table']}"
        del payload['dbms']
        del payload['table']
        if file_name not in file_list:
            file_list[file_name] = __timestamp_to_flle_name(payload['timestamp'])
            file_name += f".{file_list[file_name]}.json"
            file_path = os.path.join(data_dir, file_name)
            status = __write_to_file(file_path=file_path, payload=payload, append=False, compress=compress, exception=exception)
        else:
            file_name += f".{file_list[file_name]}.json"
            file_path = os.path.join(data_dir, file_name)
            status = __write_to_file(file_path=file_path, payload=payload, append=True, compress=compress, exception=exception)

    return status
