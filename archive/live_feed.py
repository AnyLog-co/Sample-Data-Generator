import cv2
import numpy
import timestamp_generator

def __take_photo(camera_id:int) -> (numpy.ndarray):
    """
    Take a photo to be stored
    :args:
        camera_id:int - camera to take a photo with
        exception:bool - whether to print exceptions
    :params:
        cv2_content:cv2.VideoCapture - captured image
        frame:numpy.ndarry - captured photo as an array
    :return:
        frame
    """
    cv2_content = None
    frame = None

    try:
        cv2_content = cv2.VideoCapture(camera_id)
    except Exception as error:
        print(f"Failed to take photo with camera ID {camera_id} (Error: {error})")

    if cv2_content is not None:
        try:
            _, frame = cv2_content.read()
        except Exception as error:
            print(f"Failed to read content for image (Error: {error})")

    return frame

def list_ports():
    """
    Validate available camera ports - once out of bounds, will stop
    :based-on:
        https://stackoverflow.com/questions/57577445/list-available-cameras-opencv-python
    :params:
        status:bool
        total_ports:int - number of open camera ports
    :return:
        list of open camera ports
    """
    status = True
    total_ports = 0

    while status is True:
        camera = cv2.VideoCapture(total_ports)
        if not camera.isOpened():
            status = False
        else:
            is_reading, _ = camera.read()
            if is_reading:
                print(f"Port {total_ports} is working and reads images")
            else:
                print(f"Port {total_ports} is working, but cannot read images")
        total_ports += 1

    return list(range(total_ports))

def generate_reading(db_name:str, table_name:str, camera_id:int):
    payload = {
        "camera": camera_id,
        "frame": __take_photo(camera_id=camera_id)
    }
    reading = {
        "dbms": db_name,
        "table": table_name,
        "reading": [timestamp_generator.include_timestamp(payload=payload, timezone='utc', enable_timezone_range=False,
                                                        performance_testing=False)]
    }

    return reading