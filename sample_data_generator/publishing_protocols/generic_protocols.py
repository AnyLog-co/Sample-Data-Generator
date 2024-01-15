import os
import time
import json
from src.support.__support__ import json_dumps


def print_results(payloads:list):
    """
    Print payloads one line at a time
    :args:
        payloads:list - list of payloads
    :return:
        print output per payload
    """
    for payload in payloads:
        print(json_dumps(payloads=payload, indent=None))


def file_results(payloads:list, data_dir:str, data_type:str, exception:bool=False):
    """
    Write results to file
    :args:
        payloads:list - results to write to file
        data_dir:str - directory to store data in
        exception:bool - whether to print exceptions
    :params:
        dbname:str - database name
        table:str - table name
        dir_name:str - extend path of data_dir
        file_name:str - file name ({dbname}.{table}.0.{random_int}.json)
        full_path:str - dir_name + file_name
    """
    table = payloads[0]['table']
    if data_type in ['images']:
        dbname = payloads[0]["dbms"]
    elif data_type in ['ping', 'perentagecpu']:
        dbname = payloads[0]['db_name']
    else:
        dbname = payloads[0]["dbname"]

    dir_name = os.path.expandvars(os.path.expanduser(data_dir))
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    file_name = f"{dbname}.{table}.0.{int(time.time())}.json"
    full_path = os.path.join(dir_name, file_name)

    try:
        with open(full_path, 'w') as f:
            for payload in payloads:
                del payload["table"]
                if data_type in ['images']:
                    del payload["dbms"]
                elif data_type in ['ping', 'perentagecpu']:
                        del payload['db_name']
                else:
                    del payload["dbname"]
                try:
                    json.dump(payload, f)
                except Exception as error:
                    if exception is True:
                        print(f"Failed to write content into {full_path} (Error: {error})")
                else:
                    if payload != payloads[-1]:
                        f.write(",")
                    f.write("\n")
    except Exception as error:
        if exception is True:
            print(f"Failed to open {full_path} (Error: {error})")


