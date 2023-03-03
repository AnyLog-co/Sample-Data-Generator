# Query: sql test extend=(+node_name, @ip, @port, @dbms_name, @table_name) and format = json  select  timestamp, camera , file, value, unit from sample_data2 order by timestamp desc --> selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file)
import datetime
import json
import numpy
import random
import requests
import cv2


def __list_ports():
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


def __convert_data(data:dict)->str:
    """
    If data is of type dict convert to JSON
    :args:
        data:dict - data to convert
    :params:
        json_data:str - data as a JSON
    :return:
        json_data
    """
    json_data = data
    if isinstance(data, dict):
        try:
            json_data = json.dumps(data)
        except Exception as e:
            print('Failed to convert data into JSON (Error: %s)' % e)
    return json_data


def take_photo(camera_id:int)->(numpy.ndarray):
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


def post_data(conn:str, payload:dict, topic:str='livefeed')->bool:
    """
    Send data via REST using PUT command
    :url:
        https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#using-a-post-command
    :args:
        conn:str - IP & Port of rest connection
        payload:dict - content to store in database
            - dbname
            - table
            - readings (timestamp, image, other information)
        topic:str - REST POST topic name
    :params:
        status:bool
        headers:dict - REST header
    :return:
        False if fails, else True
    """
    status = True
    headers = {
        'command': 'data',
        'topic': topic,
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }
    print(datetime.datetime.now())
    try:
        r = requests.post('http://%s' % conn, headers=headers, data=__convert_data(data=payload))
    except Exception as e:
        print('Failed to send data via POST against %s (Error: %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            status = False
            print('Failed to send data via PUT against %s due to network error: %s' % (conn, r.status_code))
    print(datetime.datetime.now())
    return status


def main(camera_id:int=0, conn:str="10.0.0.184:32149", dbms:str="test", table:str="sample_data2", topic:str="livefeed"):
    """
    Main for sending data over POST
    :args:
        camera_id:int - camera to use
        conn:str - REST connection information
        dbms:str - logical database name
        table:str - table to store data in
        topic:str - POST topic for `run mqtt`
    :params:
        frame:numpy.ndarry - image as a ndarry
        data:dict - payload / content to store
    :return:
        print "success" if image succeeds to get published
    """
    frame = take_photo(camera_id=camera_id)

    data = {
        'dbms': dbms,
        'table': table,
        "readings": [{
            'ts': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "camera": 0,
            'frame': json.dumps(frame.tolist()),
            'value': random.random(),
            'unit': 'Celsius'
        }]
    }

    if post_data(conn=conn, payload=data, topic=topic):
        print("Success")


if __name__ == '__main__':
    camera_ids = __list_ports()
    main(camera_id=random.choice(camera_ids), conn="10.0.0.184:32149", dbms="test", table="sample_data2", topic="livefeed")