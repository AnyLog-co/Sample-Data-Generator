import base64
import datetime
import hashlib
import json
import os
import uuid


def create_timestamp(increase_ts:float=0):
    timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=increase_ts)
    return timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def serialize_data(payload):
    return json.dumps(payload)


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

def file_processing(file_name:str, exception:bool=False):
    """
    read content from file and convert to base64 - used for both images and blobs
    :steps:
        1. read file
        2. base64 encode file
        3. base64 decode ASCII
    :args:
        file_name:str - file to process
        exception:bool - whether to print exceptions
    :params:

        file_content - content from file
        full_file_path:str - full path of file_name
    """
    file_content = None
    base64_bytes = None
    full_file_path = os.path.expanduser(os.path.expandvars(file_name))

    try:
        with open(file_name, 'rb') as f:
            try:
                content  = f.read()
            except Exception as error:
                if exception is True:
                    print(f"Failed to read content from file {file_name} (Error: {error})")
    except Exception as error:
        if exception is True:
            print(f"Failed to open file {file_name} to be read (Error: {error})")
    else:
        try:
            base64_bytes = base64.b64encode(content)
        except Exception as error:
            status = False
            if exception is True:
                print(f'Failed to encode file data (Error: {error})')
        else:
            try:
                file_content = base64_bytes.decode('ascii')
            except Exception as error:
                if exception is True:
                    print(f'Failed to convert encoded message to ASCII based value (Error: {error})')

        return file_content


def read_json_file(file_path:str, exception:bool=False):
    try:
        with open(file_path, 'rb') as f:
            try:
                return json.load(f)
            except Exception as error:
                if exception is True:
                    print(f"Failed to read content in {file_path} (Error: {error})")
    except Exception as error:
        if exception is True:
            print(f"Failed to open file {file_path} (Error: {error})")
    return None