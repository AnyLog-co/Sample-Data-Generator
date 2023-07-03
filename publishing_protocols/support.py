import argparse
import gzip
import hashlib
try:
    import io
except:
    pass
import importlib
import json
import os
import re
import uuid



def validate_conn_pattern(conns:str)->str:
    """
    Validate connection information format is connect
    :valid formats:
        127.0.0.1:32049
        user:passwd@127.0.0.1:32049
    :args:
        conn:str - REST connection information
    :params:
        pattern1:str - compiled pattern 1 (127.0.0.1:32049)
        pattern2:str - compiled pattern 2 (user:passwd@127.0.0.1:32049)
    :return:
        if fails raises Error
        if success returns conn
    """
    pattern1 = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')
    pattern2 = re.compile(r'^\w+:\w+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')

    for conn in conns.split(","):
        if not pattern1.match(conn) and not pattern2.match(conn):
            raise argparse.ArgumentTypeError(f'Invalid REST connection format: {conn}')

    return conns


def validate_row_size(row_size)->int:
    """
    Validate row user inputted row size 
    :args: 
        row_size - user inputted row size 
    :return: 
        row size (if correct) as prints error
    """
    try:
        value = int(row_size)
    except Exception as error:
        output = argparse.ArgumentTypeError(f"User input value {row_size} is not of type integer (Error: {error})")
    else:
        if value < 0:
            output = argparse.ArgumentTypeError(f"User input value must be greater or equal to 0")
        else:
            output = value

    return output

def validate_packages(is_blobs:bool=False, is_traffic:bool=False):
    """
    Validate Packages
    """
    try:
        import paho.mqtt
    except ImportError as error:
        raise argparse.ArgumentTypeError(f"Missing package: paho.mqtt (Error: {error}). cannot continue")
    try:
        import pytz
    except ImportError as error:
        raise argparse.ArgumentTypeError(f"Missing package: pytz (Error: {error}). cannot continue")

    if is_traffic is True:
        if not importlib.import_module("geopy"):
            raise argparse.ArgumentTypeError(f"Missing package: geopy. cannot continue")
    if is_blobs is True:
        for package in ['base64', 'io', 'cv2', 'numpy']:
            if not importlib.import_module(package):
                raise argparse.ArgumentTypeError(f"Missing package: {package}. cannot continue")



def validate_conversion_type(conversion_type:str)->str:
    """
    Check whether the user inputted a valid conversion type and whether the proper packages are imported
    :args:
        conversion_type:str - user input
    :raise:
        raise an error if invalid arg or package is not installed
    :return:
        conversion_type
    """
    if conversion_type not in ['base64', 'bytesio', 'opencv']:
        raise argparse.ArgumentTypeError(f"Invalid option {conversion_type}. Supported types: base64, bytesio, cv2")
    elif conversion_type == 'base64' and  importlib.import_module("base64") is None:
        raise argparse.ArgumentTypeError(f"Unable to locate package base64 for conversion type {conversion_type}")
    elif conversion_type == 'bytesio' and importlib.import_module('io') is None:
        raise argparse.ArgumentTypeError(f"Unable to locate package io for conversion type {conversion_type}")
    elif conversion_type == 'opencv' and importlib.import_module('cv2') is None:
        raise argparse.ArgumentTypeError(f"Unable to locate package opencv2-python for conversion type {conversion_type}")

    return conversion_type

def json_dumps(payloads:dict, print_output:bool=False)->str:
    """
    Convert dictionary to string
    :args:
        payloads:dict - data to convert
    :return:
        converted data, if fails return original data
    """
    indent = 0
    if print_output is True:
        indent = 4
    try:
        return json.dumps(payloads, indent=indent)
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

