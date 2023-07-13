import ast


def __write_file(file_path:str, content:bytes, exception:bool=False)->bool:
    status = True
    try:
        with open(file_path, 'wb') as f:
            try:
                f.write(content)
            except Exception as error:
                status = False
                if exception is True:
                    print(f"Failed to write content into {file_path} (Error: {error})")
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to opne file {file_path} (Error: {error})")

    return  status


def convert_base64(content:str, file_path:str, exception:bool=False)->bool:
    """
    Convert base64 string back to bytes in order to write into file
    :args:
        content:str - content to convert
        exception:bool - whether to print exceptions
    :params:
        status:bool
        raw_content:bytes - converted content into bytes
    :return:
        status, raw_content
    """
    status = True
    raw_content = None
    try:
        import base64
    except Exception as error:
        if exception is True:
            print(f"base64 not installed (Error: {error})")
        return False

    try:
        raw_content = base64.b64decode(content)
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to decode content (Error: {error}")

    return __write_file(file_path=file_path, content=raw_content, exception=exception)


def convert_opencv(content:str, file_path:str, exception:bool=False):
    """
    Convert cv2 format back into ndarry
    :args:
        content:str - content to convert
        exception:bool - whether to print exceptions
    :params:
        status:bool
        raw_content:bytes - converted content into bytes
    :return:
        status, raw_content
    """
    status = True
    raw_content = None
    try:
        import cv2
        import numpy
    except Exception as error:
        if exception is True:
            print(f"cv2 and/or numpy not installed (Error: {error})")
        return False

    if not isinstance(content, numpy.ndarray) or not isinstance(content, list):
        try:
            content = ast.literal_eval(content)
        except Exception as error:
            status = False
            if exception is True:
                print(f"Failed to convert content to natural form (Error: {error})")

    if status is True and not isinstance(content, numpy.ndarray):
        try:
            raw_content = numpy.array(content)
        except Exception as error:
            status = True
            if exception is True:
                print(f"Failed to convert content into ndarry format (Error: {error})")

    if status  is True and isinstance(content, numpy.ndarray):
        raw_content = content

    if status is True and isinstance(raw_content, numpy.ndarray):
        try:
            cv2.imwrite(file_path, raw_content)
        except Exception as error:
            status = False
            if exception is True:
                print(f"Failed to store image in file {file_path} (Error: {error})")

    return  status


def main(content:str, conversion_type:str, file_path:str, exception:bool=False)->(bool, bytes):
    status = True
    raw_content = None
    if conversion_type == "base64":
        status = convert_base64(content=content, file_path=file_path, exception=exception)
    elif conversion_type == "bytesio":
        status = __write_file(file_path=file_path, content=content, exception=exception)
    elif conversion_type == "opencv":
        status = convert_opencv(content=content, file_path=file_path, exception=exception)

    return status
