import os
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).rsplit('data_generators', 1)[0]
PROTOCOLS = os.path.join(ROOT_PATH, 'protocols')
sys.path.insert(0, PROTOCOLS)
from support import decompress_file
from support import json_loads


def __extract_table_name(file_name)->str:
    """
    Extract table name from file path
    :example:
        new_table.json --> new_table
        db_name.new_table.0.0json --> new_table
    :args:
        file_name:str - file to extract table name from
    :params:
        table_name:str - table name
    :return:
        table_name
    """
    table_name = None
    file_parts = file_name.split('.')

    if len(file_parts) == 2:
        table_name = file_parts[0]
    else:
        table_name = file_parts[1]

    return table_name.lower().replace('-', '_')


def __read_file(file_path:str, exception:bool=False)->list:
    """
    Read content from file
    :args:
        file_path:str - file to read content from
        exception:bool - whether or not to print exception(s)
    :params:
        content:str -
    """
    content = []
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as f:
                try:
                    for line in f.read().split('\n'):
                        if line != '':
                            content.append(json_loads(data=line))
                except Exception as e:
                    if exception is True:
                        print(f'Failed to read content in {file_path} (Error: {e})')
        except Exception as e:
            if exception is True:
                print(f'Failed to open file {file_path} (Error: {e})')
    return content


def read_data(dir_path:str, compress:bool=False, exception:bool=False)->dict:
    """
    Read data from file(s)
    :args:
        dir_path:str - directory containing data to be stored
        compress:bool - whether to decompress files and recompress them
        exception:bool - whether to print exception(s)
    :params:
        file_content:dict - dict of lists with content from files
    :return:
        file_content
    """
    files_content = {}
    if not os.path.isdir(dir_path):
        if exception is True:
            print(f'Failed to locate directory {dir_path}')
        return files_content

    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if compress is True:
            file_path = decompress_file(compressed_file=file_path, exception=exception)

        table_name = __extract_table_name(file_name=file_name)
        if table_name not in files_content:
            files_content[table_name] = __read_file(file_path=file_path, exception=exception)
        else:
            files_content[table_name] = [*files_content[table_name],
                                         *__read_file(file_path=file_path, exception=exception)]
        if compress is True:
            os.remove(file_path)

    return files_content
