import base64


def __read_image(file_name:str, exception:bool=False)->(bool, bytes):
    """
    Get content in file as binary
    :args:
        file_name:str - file path
        exception:bool - whether or not to write exceptions
    :params:
        status:bool
        file_data:bytes - content in file read as binary
        full_path:str - full path of file_name
    :return:
        status, file_data
    """
    status = True
    file_data = None
    try:
        with open(file_name, 'rb') as fb:
            try:
                file_data = fb.read()
            except Exception as error:
                if exception is True:
                    print(f'Failed to read content as binary from {file_name} (Error: {error})')
                status = False
    except Exception as error:
        if exception is True:
            print(f'Failed to binary-open {file_name} (Error: {error})')
        status = False

    return status, file_data


def __convert_base64(file_data:bytes, exception:bool)->(bool, str):
    """
    Convert bytes to ASCII string
    :args:
        file_data:bytes - bytes content generated by __read_image
        exception:bool - whether or not to print exception(s)
    :params:
        status:bool
        base64_bytes:bytes - encoded file_data
        base64_msg:string - encode file_data (base64_bytes) as string
    :return:
        status, base64_msg
    """
    status = True
    base64_bytes = None
    base64_msg = None
    try:
        base64_bytes = base64.b64encode(file_data)
    except Exception as error:
        if exception is True:
            print(f'Failed to encode file data (Error: {error})')
        status = False
    if status is True and isinstance(base64_bytes, bytes):
        try:
            base64_msg = base64_bytes.decode('ascii')
        except Exception as error:
            if exception is True:
                print(f'Failed to convert encoded message to ASCII based value (Error: {error})')
            status = False

    return status, base64_msg


def main(file_name:str, exception:bool=False)->dict:
    """
    Given image file(s), read information and store into dictionary
    :args:
        file_name:str - (comma seperated list of) file name(s)
        exception:bool - whether or not to print exception(s) to screen
    :params:
        files:dict - dictionary of (full path) file names + raw data as string binary
    :return:
        files
    """
    base64_msg = None

    status, binary_file = __read_image(file_name=file_name, exception=exception)

    if status is False or binary_file is None:
        print(f'Failed to to process file {file_name}')
    elif isinstance(binary_file, bytes):
        status, base64_msg = __convert_base64(file_data=binary_file, exception=exception)
        if status is False or not isinstance(base64_msg, str):
            base64_msg = None

    return base64_msg



