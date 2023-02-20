import cv2
import numpy
import os
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split('data_generators')[0]
PUBLISHING_PROTOCOL = os.path.join(ROOT_PATH, 'publishing_protocol')
sys.path.insert(0, PUBLISHING_PROTOCOL)

from publishing_protocols.support import json_dumps



def __read_file(file_name:str, exception:bool=False)->(bool, numpy.ndarray):
    status = True
    frame = None

    if os.path.isfile(file_name):
        try:
            vid = cv2.VideoCapture(file_name)
        except Exception as error:
            status = False
            if exception is True:
                print(f"Failed to open {file_name} (Error: {error})")
    else:
        status = False
        if exception is True:
            print(f"Failed to locate {file_name}")

    if status is True:
        try:
            status, frame = vid.read()
        except Exception as error:
            status = False
            if exception is True:
                print(f"Failed to read content from {file_name} (Error: {error})")

    return status, frame


def __convert_to_list(frame:numpy.ndarray, exception:bool=False)->str:
    output = None
    try:
        list_frame = frame.tolist()
    except Exception as error:
        if exception is True:
            print(f"Failed to convert frame into a list (Error: {error})")
    else:
        output = json_dumps(payloads=list_frame)

    return output

def main(file_name:str, exception:bool=False)->list:
    output = None
    status, frame = __read_file(file_name=file_name, exception=exception)
    if status is True and frame is not None:
        output = __convert_to_list(frame=frame, exception=exception)

    return output




