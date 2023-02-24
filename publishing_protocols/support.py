import datetime
import gzip
import hashlib
import io
import json
import os
import uuid
try:
    import pytz
except:
    pass
import random


def json_dumps(payloads:dict)->str:
    """
    Convert dictionary to string
    :args:
        payloads:dict - data to convert
    :return:
        converted data, if fails return original data
    """
    try:
        return json.dumps(payloads)
    except Exception as error:
        return payloads


def json_loads(data:str)->dict:
    """
    Convert dictionary to dict
    :args:
        data:str - data to convert
    :return:
        converted data, if fails return original data
        """
    try:
        return json.loads(data)
    except Exception as e:
        return data


def payload_conversions(payloads:dict, dbms:str, table:str)->list:
    """
    For POST & MQTT functions, convert the content to have complete dicts
    :args:
        payloads:dict - either a dictionary or list of content to be stored in database
        dbms:str - logical database name
        table:str - table name, if payloads is dict use keys as table name
    :params:
        update_payloads:list - list of updated payloads
    """
    updated_payloads = []
    if isinstance(payloads, dict):
        for table in payloads:
            for row in payloads[table]:
                row['dbms'] = dbms
                row['table'] = table
                updated_payloads.append(json_dumps(data=row))
    elif isinstance(payloads, list):
        for row in payloads:
            row['dbms'] = dbms
            row['table'] = table
            updated_payloads.append(json_dumps(data=row))

    return updated_payloads


def compress(input_file:str, exception:bool=False)->bool:
    """
    compress file - if successful, remove input_file
    :args:
        input_file:str - file to compress
        exception:bool - whether to print exception(s)
    :params:
        status:bool
        compress_file_name:str - file_name + .gz
    :return:
        status
    """
    status = False
    compress_file_name = input_file + '.gz'
    try:
        with open(input_file, 'rb') as rf:
            try:
                with open(compress_file_name,'wb') as wf:
                    try:
                        wf.write(gzip.compress(rf.read()))
                    except Exception as e:
                        if exception is True:
                            print(f'Failed to compress {input_file} (Error: {e})')
            except Exception as e:
                if exception is True:
                    print(f'Failed to open compressed file {compress_file_name} (Error: {e})')
    except Exception as e:
        if exception is True:
            print(f'Failed to read file {input_file} (Error: {e})')
    else:
        status = True

    if status is True:
        os.remove(input_file)

    return status


def decompress_file(compressed_file:str, exception:bool=False)->str:
    """
    Decompress .gz file
    :args:
        compressed_file:str - file to decompress
        exception:bool - whether or not to print exceptions
    :params:
        input_file:str - decompressed file
    :return:
        input_file, if fails at any point returns None
    """
    input_file = compressed_file.rsplit('.gz', 1)[0]
    try:
        with gzip.open(compressed_file, 'rb') as rf:
            try:
                with io.TextIOWrapper(rf, encoding='utf-8') as decoder:
                    content = decoder.read()
                    try:
                        with open(input_file, 'w') as f:
                            try:
                                f.write(content)
                            except Exception as e:
                                input_file = None
                                if exception is True:
                                    print(f'Failed to write content into {input_file} (Error: {e}')
                    except Exception as e:
                        input_file = None
                        if exception is True:
                            print(f'Failed to open JSON file (Error: {e})')
            except Exception as e:
                input_file = None
                if exception is True:
                    print(f'Failed to decode content in zipped file (Error: {e})')
    except Exception as e:
        input_file = None
        if exception is True:
            print(f'Failed to open zipped file {compressed_file} (Error: {e})')
    
    return input_file


def generate_string_hash(file_name:str, data:str)->str:
    """
    based on file_name + data generate hash value
    :args:
        file_name:str - file used to generate has value
        data:str - content in file
    :params:
        str_hash:hashlib.Hash - generated hash value
    :return:
        hash value as UUID
    """
    str_hash = hashlib.md5()
    if file_name:
        # Prefixed data can be dbms name and table name that are considered in the hash
        str_hash.update(file_name.encode())  # Update the hash with the prefix data+

    str_hash.update(data.encode())  # Update the hash
    return str(uuid.UUID(str_hash.hexdigest()))


def media_type(file_suffix:str)->str:
    """
    Generate media type based on file suffix
    :args:
        file_suffix:str - file suffix
    :params:
        suffix_value:str - based on file suffix generated suffix
    :return:
        suffix_value
    """
    suffix_value = 'unknown'
    if file_suffix == 'png':
        suffix_value = 'image/png'
    elif file_suffix in ['jpg', 'jpeg']:
        suffix_value = 'image/jpeg'
    elif file_suffix == 'mp4':
        suffix_value = 'video/mp4'

    return suffix_value