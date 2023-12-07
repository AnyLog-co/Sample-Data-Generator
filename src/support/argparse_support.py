import argparse
import importlib
import os.path
import re

import src.publishing_protocols.publish_data as publish_data

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
            raise argparse.ArgumentTypeError(f'Invalid connection format: {conn}. Supported formats: 127.0.0.1:32049 or user:passwd@127.0.0.1:32049')

    return conns

def validate_row_size(row_size)->int:
    """
    Validate row  size inputted by user
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

def validate_sleep_time(sleep)->int:
    """
    Validate sleep inputted by user
    :args:
        sleep - user inputted wait time
    :return:
        row size (if correct) as prints error
    """
    try:
        value = float(sleep)
    except Exception as error:
        output = argparse.ArgumentTypeError(f"User input value {sleep} is not of type integer or float (Error: {error})")
    else:
        if value < 0:
            output = argparse.ArgumentTypeError(f"User input value must be greater or equal to 0")
        else:
            output = value

    return output

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
    error = ""
    if conversion_type not in ['base64', 'bytesio', 'opencv']:
        error = f"Invalid option {conversion_type}. Choices: base64, bytesio, opencv"
    elif conversion_type == 'base64' and  importlib.import_module("base64") is None:
        error = "Unable to locate package base64 for conversion type {conversion_type}"
    elif conversion_type == 'bytesio' and importlib.import_module('io') is None:
        error = f"Unable to locate package io for conversion type {conversion_type}"
    elif conversion_type == 'opencv' and importlib.import_module('cv2') is None:
        error = f"Unable to locate package opencv2-python for conversion type {conversion_type}"

    if error != "":
        raise argparse.ArgumentError(error)

    return conversion_type

def __prepare_conns(conn:str, insert_process:str, exception:bool=False):
    conns = conn.split(',')
    if insert_process is 'mqtt':
        conns = publish_data.connect_mqtt(conns, exception=exception)
        if not conns:
            print("Failed to set connection for MQTT publisher")
            exit(1)
    elif insert_process in ["post", "put"]:
        conns = publish_data.setup_put_post_conn(conns=conns)

    return conns

def prepare_configs(batch_size:int, data_type:str, conversion_type:str):
    if batch_size == 0:
        batch_size = 1

    data_type = data_type.split(",")
    if ('images' in data_type or 'cars' in data_type or 'people' in data_type) and conversion_type is None:
        conversion_type = 'base64'

    return  batch_size, conversion_type