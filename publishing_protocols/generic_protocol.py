import datetime
import json
import gzip
import os
import time
import support


ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('protocols', 1)[0]

import file_processing

def __timestamp_to_file_name(orig_timestamp:str)->int:
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
        try:
            timestamp = int(datetime.datetime.strptime(orig_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())
        except Exception as error:
            timestamp = str(time.time()).split('.')[0]

    return timestamp


def __write_blob(file_path:str, payload:dict, compress:bool, blob_data_type:str, conversion_type:str,
                 exception:bool=False)->dict:
    blob = None
    if blob_data_type == "image" and "file_content" in payload:
        blob = payload["file_content"]
    elif blob_data_type == "video" and "readings" in payload and "binaryValue" in payload["readings"]:
        blob = payload["readings"]["binaryValue"]
    elif conversion_type == 'bytesio' and blob_data_type == 'image':
        payload['file_content'] = payload['file_content'].__str__()
    elif conversion_type == 'bytesio' and blob_data_type == 'video':
        payload["readings"]["binaryValue"] = payload['file_content'].__str__()

    return payload


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

    if isinstance(payloads, list):
        for payload in payloads:
            file_name = f"{payload['dbms']}.{payload['table']}"
            del payload['dbms']
            del payload['table']

            if file_name not in file_list:
                file_list[file_name] = __timestamp_to_file_name(payload['timestamp'])
                file_name += f".{file_list[file_name]}.json"
                file_path = os.path.join(data_dir, file_name)
                append=False
            else:
                file_name += f".{file_list[file_name]}.json"
                file_path = os.path.join(data_dir, file_name)
                append = True
            status = __write_to_file(file_path=file_path, payload=payload, append=append, compress=compress,
                                     exception=exception)
    else:
        if 'dbName' in payloads:
            dbms = payloads['dbName']
            del payloads['dbName']
        else:
            dbms = payloads['dbms']
            del payloads['dbms']
        if 'deviceName' in payloads:
            table = payloads['deviceName']
            del payloads['deviceName']
        else:
            table = payloads['table']
            del payloads['table']

        file_name = f"{dbms}.{table}"

        if file_name not in file_list:
            if 'timestamp' in payloads:
                file_list[file_name] = __timestamp_to_file_name(payloads['timestamp'])
            else:
                file_list[file_name] = __timestamp_to_file_name(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            file_name += f".{file_list[file_name]}.json"
            file_path = os.path.join(data_dir, file_name)
            append = False
        else:
            file_name += f".{file_list[file_name]}.json"
            file_path = os.path.join(data_dir, file_name)
            append = True
        status = __write_to_file(file_path=file_path, payload=payloads, append=append, compress=compress,
                                 exception=exception)

    return status


def write_blob_to_file(payloads:dict, data_dir:str=os.path.join(ROOT_PATH, 'data'), compress:bool=False,
                       blob_data_type:str='', conversion_type:str="base64", exception:bool=False)->bool:
    append = False
    status = True

    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    if blob_data_type == 'image':
        blob_file_name = os.path.join(data_dir, f"{payloads['dbms']}.{payloads['table']}.{payloads['file_name']}")
        json_file_name = blob_file_name.rsplit(".", 1)[0] + ".json"
        blob = payloads['file_content']
        del payloads['dbms']
        del payloads['table']
        del payloads['file_name']
        del payloads['file_content']
    elif blob_data_type == 'video':
        blob_file_name = os.path.join(data_dir, f"{payloads['dbName']}.{payloads['device_name']}.{payloads['origin']}.mp4")
        if conversion_type == "opencv":
            blob_file_name = blob_file_name.replace(".mp4", "png")
        json_file_name = blob_file_name.rsplit(".", 1)[0] + ".json"
        blob = payloads['readings']['binaryValue']
        del payloads['dbName']
        del payloads['device_name']
        del payloads['readings']['binaryValue']

    status = file_processing.main(content=blob, conversion_type=conversion_type, file_path=blob_file_name,
                                  exception=exception)

    if status is False and blob_data_type == 'image':
        payloads['file_content'] = blob
    elif status is False and blob_data_type == 'video':
        payloads['readings']['binaryValue'] = blob

    if os.path.isfile(json_file_name):
        append = True

    status = __write_to_file(file_path=json_file_name, payload=payloads, append=append, compress=compress,
                             exception=exception)










