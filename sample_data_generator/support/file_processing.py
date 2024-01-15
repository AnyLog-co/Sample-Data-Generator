import json
import os

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


def __convert_base64(file_name:str, exception:bool=False)->(bool, str):
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


def __convert_bytesio(file_name:str, exception:bool=False)->(bool, str):
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
    # if status is True and isinstance(bytesio_bytes, bytes):
    #     try:
    #         file_content = bytesio_bytes.decode('ascii')
    #     except Exception as error:
    #         status = False
    #         if exception is True:
    #             print(f'Failed to convert encoded message to ASCII based value (Error: {error})')

    return status, file_content


def __convert_opencv(file_name:str, exception:bool=False)->(bool, str):
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
            file_content = json.dumps(payloads=list_frame)

    return status, file_content


def file_processing(conversion_type:str, file_name:str, exception:bool=False)->(bool, str):
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
        status, file_content = __convert_base64(file_name=full_file_path, exception=exception)
    elif conversion_type == "bytesio":
        status, file_content = __convert_bytesio(file_name=full_file_path, exception=exception)
    elif conversion_type == "opencv":
        status, file_content = __convert_opencv(file_name=file_name, exception=exception)
    else:
        print(f"Unable to convert to format {conversion_type}")
        exit(1)

    return file_content




