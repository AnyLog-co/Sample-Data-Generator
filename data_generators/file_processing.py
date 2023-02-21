import argparse
import importlib
import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split('data_generators')[0]
PUBLISHING_PROTOCOL = os.path.join(ROOT_PATH, 'publishing_protocol')
sys.path.insert(0, PUBLISHING_PROTOCOL)

from publishing_protocols.support import json_dumps


def __read_file(file_name:str, exception:bool=False)->bytes:
    """
    Get content in file as binary
    :args:
        file_name:str - file to read
        exception:bool - whether to print exceptions
    :params:
        content:bytes - content read from file
    :return:
        content
    """
    content = None
    try:
        with open(file_name, 'rb') as f:
            try:
                content = f.read()
            except Exception as error:
                if exception is True:
                    print(f"Failed to read content from file {file_name} (Error: {error})")
    except Exception as error:
        if exception is True:
            print(f"Failed to open file {file_name} to be read (Error: {error})")

    return content


def check_conversion_type(arg):
    """
    Check whether the user inputted a valid conversion type and whether the proper packages are imported
    :args:
        arg - user input
    :raise:
        raise an error if invalid arg or package is not installed
    :return:
        arg
    """
    if arg not in ['base64', 'bytesio', 'cv2']:
        raise argparse.ArgumentTypeError(f"Invalid option {arg}. Supported types: base64, bytesio, cv2")
    elif arg == 'base64' and  importlib.util.find_spec("base64") is None:
        raise argparse.ArgumentTypeError(f"Unable to locate package base64 for conversion type {arg}")
    elif arg == 'bytesio' and importlib.util.find_spec('io') is None:
        raise argparse.ArgumentTypeError(f"Unable to locate package io for conversion type {arg}")
    elif arg == 'cv2' and importlib.util.find_spec('cv2') is None:
        raise argparse.ArgumentTypeError(f"Unable to locate package opencv2-python for conversion type {arg}")

    return arg


def convert_base64(file_name:str, exception:bool=False)->(bool, str):
    """
    Convert file to base64
        - read content (binary format)
        - encode raw content
        - convert encoded content to ASCII format
    :args:
        file_name:str - file to be read
        exception:bool - whether to print exceptions
    :params:
        status:bool
        file_content:str - convert bytes to ASCII format
        raw_content:bytes - read file content
        base64_bytes:bytes - encoded file content
    :return:
        status, file_content
    """
    import base64
    status = True
    file_content = None
    raw_content = __read_file(file_name=file_name, exception=exception)

    if raw_content is not None: # encode raw_content if able to read content
        try:
            base64_bytes = base64.b64encode(raw_content)
        except Exception as error:
            status = False
            if exception is True:
                print(f'Failed to encode file data (Error: {error})')
    else:
        status = False

    if status is True and isinstance(base64_bytes, bytes): # convert bytes to ASCII format
        try:
            file_content = base64_bytes.decode('ascii')
        except Exception as error:
            status = False
            if exception is True:
                print(f'Failed to convert encoded message to ASCII based value (Error: {error})')

    return status, file_content


def convert_bytesio(file_name:str, exception:bool=False)->(bool, str):
    """
    Convert file to base64
        - read content (binary format)
        - convert content to be BytesIO
        - read content
    :args:
        file_name:str - file to be read
        exception:bool - whether to print exceptions
    :params:
        status:bool
        file_content:str - convert bytes to ASCII format
        raw_content:bytes - read file content
        bytesio_bytes:bytes - encoded file content
    :return:
        status, fle_content
    """
    import io
    status = True
    file_content = None
    bytesio_bytes = None
    raw_content = __read_file(file_name=file_name, exception=exception)

    try:
        bytesio_bytes = io.BytesIO(raw_content)
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to convert file content into byte format (Error: {error})")

    if status is True and isinstance(bytesio_bytes, io.BytesIO):
        try:
            file_content = bytesio_bytes.read()
        except Exception as error:
            status = False
            if exception is True:
                print(f"Failed to read content from file (Error: {error})")

    return status, file_content


def convert_cv2(file_name:str, exception:bool=False)->(bool, str):
    """
    Convert file to cv2
        - read content (binary format)
        - capture an image from video
        - read video
        - convert to list & serialize
    :args:
        file_name:str - file to be read
        exception:bool - whether to print exceptions
    :params:
        status:bool
        file_content:str - serialized file content
        cv2_content - video capture
    :return:
        status, file_content
    """
    import cv2
    status = True
    file_content = None
    cv2_content = None
    frame = None

    try: # capture an image
        cv2_content = cv2.VideoCapture(file_name)
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to capture content from {file_name} (Error: {error})")

    if status is True and cv2_content is not None: # read video
        try:
            status, frame = cv2_content.read()
        except Exception as error:
            status = False
            if exception is True:
                print(f"Failed to read content from {file_name} (Error: {error})")

    if status is True and frame is not None: # convert to list & serialize
        try:
            list_frame = frame.tolist()
        except Exception as error:
            if exception is True:
                print(f"Failed to convert frame into a list (Error: {error})")
        else:
            file_content = json_dumps(payloads=list_frame)

    return status, file_content


def main(conversion_type:str, file_name:str, exception:bool=False)->(bool, str):
    """
    main for file processing
    :args:
        conversion_type:str - conversion type
        file_name:str - file to process
        exception:bool - whether to print exceptions
    :params:
        status:bool
        file_content - content from file
        full_file_path:str - full path of file_name
    """
    status = True
    file_content = None
    full_file_path = os.path.expanduser(os.path.expandvars(file_name))

    if not os.path.isfile(full_file_path):
        status = False
        if exception is True:
            print(f"Failed to locate {file_name} - cannot continue.")
        return status, file_content

    if conversion_type == "base64":
        status, file_content = convert_base64(file_name=full_file_path, exception=exception)
    elif conversion_type == "bytesio":
        status, file_content = convert_bytesio(file_name=full_file_path, exception=exception)
    elif conversion_type == "cv2":
        status, file_content = convert_cv2(file_name=file_name, exception=exception)

    return file_content
