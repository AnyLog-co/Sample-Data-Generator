import argparse
import csv
import datetime
import json
import os
import time

from extract_info import *
from mqtt import *

DATA_DIR = os.path.join(os.path.expandvars(os.path.expanduser(__file__)).split('nvidia_normalizing')[0], 'data')
TIMESTAMP_FORMAT = '%Y-%m-%d::%H:%M:%S'

def __test_timestamp(start_timestamp:str)->str:
    """
    Validate timestamp value is of the correct format
    :args:
        start_timestamp:str - Start timestamp
    :raise:
        if format is not %Y-%m-%d %H:%M:%S then return error
    :return:
        start_timestamp manipulated to be used by the NVIDIA code base
    """
    try:
        datetime.datetime.strptime(start_timestamp, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        if start_timestamp is not None:
            raise argparse.ArgumentTypeError(f"Invalid Format for timestamp value: '{start_timestamp}' (Error: {e})\n\tExpected Format: 'YYYY-MM-DD HH:MM:SS'")
    return start_timestamp.replace(" ", "::")


def __test_data_directory(data_dir:str)->str:
    """
    Given the directory where files will be saved, validate its existance
    :args:
        data_dir:str - directory where data will be stored
    :params:
        full_path:str - full path of data_dir
    :raise:
        if fails to create full_path then returns error
    :return:
        full_path
    """
    full_path = os.path.expandvars(os.path.expanduser(data_dir))
    if not os.path.isdir(full_path):
        try:
            os.path.makedirs(full_path)
        except Exception as e:
            raise argparse.ArgumentTypeError(f'Failed to create directory "{full_path}" (Error: {e})')
    return full_path


def __convert_json(message:dict)->str:
    """
    Convert content from dictionary to JSON
    :args:
      messages
    :raise:
        if fails to convert raise error
    :return:
      messages as
    """
    try:
        return json.dumps(message)
    except Exception as e:
        raise Exception(f"Failed to convert message '{message}' from dictionary to JSON format (Error: {e})")


def __update_timestamps(end_time:str)->(str, str):
    """
    Given the end timestamp, generate new start and end timestamps
    :args:
        end_timestamp:str - original timestamp
    :params:
        update_start_ts:str - updated start timestamp to be 1 second after end timestamp
        update_end_ts:str - updated end timestamp
    :return:
        update_start_ts, update_end_ts
    """
    update_start_ts = (datetime.datetime.strptime(end_time, TIMESTAMP_FORMAT) + datetime.timedelta(seconds=1)).strftime(TIMESTAMP_FORMAT)
    update_end_ts = datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT)

    return update_start_ts, update_end_ts


def get_ngc_logs(start_time:str, end_time:str, system:str, location:str, component:str, data_dir:str=DATA_DIR,
                 exception:bool=False)->str:
    """
    Using `ngc  fleet-command log download` store logs into fclog.csv file
    :process:
        1. create / clean file_path
        2. generate log data
        3. validate file contains more than 1 line
    :original command:
        ngc  fleet-command log download \
            --from-date 2022-05-01::00:00:00 \
            --to-date 2022-06-01::00:00:00 \
            --system system-1 \
            --location system-2 \
            --component helm \
            --name $HOME/fclog.log
    :args:
        start_time:str - start time
        end_time:str - end time
        system:str - which system to get logs from
        location:str - location of said system
        component to get logs for
        data_dir:str - location where data will be stored
        exception:bool - whether or not to write exceptions
    :params:
        line_count:int - number of lines inf file_path
        file_path:str - full file path for CSV file
        cmd:str - (ngc) command to execute
    :raise:
        raise a valid error if unable to create CSV file or NGC command fails
    :return:
        file_path if file contains more than 1 line
        else None
    """
    line_count = 0
    file_path = os.path.join(data_dir, 'fclog.csv')
    cmd = f"ngc  fleet-command log download --from-date {start_time} --to-date {end_time} --system {system} --location {location} --component {component} --name {file_path}"
    
    if os.path.isfile(file_path): 
        try:
            os.remove(file_path) 
        except Exception as e: 
            raise f'Failed to remove file {file_path} (Error: {e})'

    try:
        os.system(cmd)
    except Exception as e:
        raise Exception(f"Failed to execute 'ngc' command (Error: {e})")

    try:
        with open(file_path, 'r') as f:
            try:
                for line in f.readlines():
                    if line != '\n':
                        line_count += 1
            except Exception as e:
                file_path = None
                if exception is True:
                    print(f'Failed to read the number of lines in {file_path} (Error: {e})')
    except Exception as e:
        file_path = None
        if exception is True:
            print(f'Failed top open file {file_path} (Error: {e})')
    else:
        if line_count <= 1:
            file_path = None

    return file_path


def mqtt_send(topic:str, db_name:str, broker:str, port:int, user:str, passwd:str, mqtt_wait:float, start_time:str,
              end_time:str, system:str, location:str, component:str, data_dir:str,  exception:bool=False):
    """
    A sub-section of main such that code would not get repeated within the actual main process
    :args:
        topic:str - MQTT topic
        db_name:str - logical database where data will be stored
        broker:str - MQTT broker
        port:int - MQTT port
        user:str  - MQTT user
        passwd:str - MQTT password correlated to user
        mqtt_wait:str - amount of time to wait between each MQTT request
        start_time:str - Default Start time (in UTC)
        end_time:str - Default End time (in UTC)
        system:str - which system to get logs from
        location:str - location of system to get logs from
        component:str - which component to information for
        data_directory:str - directory where CSV files will be coming into
    :params:
        file_path:str - file containing content from NGC command
        mqtt_connection:paho.mqtt.client.Client - connection to MQTT client
        messages:dict - formatted 'messages' section from row(s) in CSV file
        details:dict - formatted 'Additional Details' section from row(s) in CSV file
        payload:str - JSON format of messages + details
    """
    file_path = get_ngc_logs(start_time=start_time, end_time=end_time, system=system,
                             location=location, component=component, data_dir=data_dir, exception=exception)
    if file_path is not None:
        mqtt_connection = connect_mqtt_broker(broker=broker, port=port, username=user,  password=passwd,
                                              exception=exception)
        if mqtt_connection is not None:
            mqtt_connection.loop_start()
            for row in csv.DictReader(open(file_path)):
                try:
                    messsages = extract_message(db_name=db_name, message=row['Message'])
                except Exception as e:
                    messsages = {}
                    if exception is True: 
                        print(f'Failed to extract messages from "{row}" (Error: {e})')
                try:
                    details = extract_additional_details(content=row['Additional Details'])
                except Exception as e:
                    details = {}
                    if exception is True: 
                        print(f'Failed to extract additional details from "{row}" (Error: {e})')

                messsages.update(details)
                if messsages != {} and messsages != details:
                    payload = __convert_json(message=messsages)
                    send_data(mqtt_client=mqtt_connection, topic=topic, payload=payload, exception=exception)
                    time.sleep(mqtt_wait)
            mqtt_connection.loop_stop()


def print_content(db_name:str, start_time:str, end_time:str, system:str, location:str, component:str, data_dir:str,
                  exception:bool=False):
    """
    Instead of sending data via MQTT - print to screen
    :args:
        topic:str - MQTT topic
        db_name:str - logical database where data will be stored
        start_time:str - Default Start time (in UTC)
        end_time:str - Default End time (in UTC)
        system:str - which system to get logs from
        location:str - location of system to get logs from
        component:str - which component to information for
        data_directory:str - directory where CSV files will be coming into
    :params:
        file_path:str - file containing content from NGC command
        messages:dict - formatted 'messages' section from row(s) in CSV file
        details:dict - formatted 'Additional Details' section from row(s) in CSV file
        payload:str - JSON format of messages + details
    """
    file_path = get_ngc_logs(start_time=start_time, end_time=end_time, system=system,
                             location=location, component=component, data_dir=data_dir, exception=exception)
    if file_path is not None:
        for row in csv.DictReader(open(file_path)):
            try:
                messsages = extract_message(db_name=db_name, message=row['Message'])
            except Exception as e:
                messsages = {}
                if exception is True:
                    print(f'Failed to extract messages from "{row}" (Error: {e})')
            try:
                details = extract_additional_details(content=row['Additional Details'])
            except Exception as e:
                details = {}
                if exception is True:
                    print(f'Failed to extract additional details from "{row}" (Error: {e})')

            messsages.update(details)
            if messsages != {} and messsages != details:
                payload = __convert_json(message=messsages)
                print(payload)

def main():
    """
    The following gets data from NVIDA fleet_command and stores it into AnyLog via MQTT
    :process:
        1. download logs from fleet command
        2. normalize the data from CSV into JSON format
        3. send data into AnyLog via MQTT
    :requirements:
        1. access to fleet_command
        2. NVIDA's NGC tool to communicate with fleet_command
        3. AnyLog node(s) to receive the data via MQTT
    :positional arguments:
        topic                 MQTT topic
        db_name               logical database name
    :optional arguments:
        -h, --help                              show this help message and exit
    :ngc optional arguments:
        --start-time        START_TIME          Default Start time (in UTC) [Default Timestamp: '2022-06-10 16:38:14']
        --end-time          END_TIME            Default End time (in UTC) [Timestamp Format: 'YYYY-MM-DD HH:MM:SS']
        --system            SYSTEM              which system to get logs from
        --location          LOCATION            location of system to get logs from
        --component         COMPONENT           which component to information for
        --data-dir    DATA_DIRECTORY      directory where CSV files will be coming into
            [Default: '/Users/orishadmon/Sample-Data-Generator/data']
    :mqtt optional arguments:
        --broker            BROKER              MQTT Broker
        --port              PORT                MQTT port
        --user              USER                MQTT user
        --passwd            PASSWD              MQTT password correlated to user
        --mqtt-wait         MQTT_WAIT           How long to wait after each MQTT POST request
    :general optional arguments:
        --repeat            REPEAT              How many time to repeat the process. If set to 0 repeat indefinitely
            [default: 1]
        --sleep             SLEEP               How many seconds to wait between each iteration
        --print             [PRINT]             print content in file instead of sending to MQTT    [default: False]
        --exception         [EXCEPTION]         whether to print error messages or not              [default: False]
    :params:
        end_time:str - ngc download end time (set to now by default)
        file_path:str - full path of file containing contnet from
    """
    parser = argparse.ArgumentParser()
    # required info
    parser.add_argument('topic', type=str, default='test', help='MQTT topic')
    parser.add_argument('db_name', type=str, default='test', help='logical database name')

    # ngc command info
    parser.add_argument('--start-time', type=__test_timestamp, default=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                        help="Default Start time (in UTC) [Default Timestamp: '%(default)s']")
    parser.add_argument('--end-time', type=__test_timestamp, default=None,
                        help="Default End time (in UTC) [Timestamp Format: 'YYYY-MM-DD HH:MM:SS']")
    parser.add_argument('--system', type=str, default='system-1', help='which system to get logs from')
    parser.add_argument('--location', type=str, default='system-2', help='location of system to get logs from')
    parser.add_argument('--component', type=str, default='helm', help='which component to information for')
    parser.add_argument('--data-dir', type=__test_data_directory, default=DATA_DIR,
                        help="directory where CSV files will be coming into [Default: '%(default)s']")
    # mqtt info
    parser.add_argument('--broker', type=str, default='127.0.0.1', help='MQTT Broker')
    parser.add_argument('--port', type=int, default=32150, help='MQTT port')
    parser.add_argument('--user', type=str, default=None, help='MQTT user')
    parser.add_argument('--passwd', type=str, default=None, help='MQTT password correlated to user')
    parser.add_argument('--mqtt-wait', type=float, default=0.5, help='How long to wait after each MQTT POST request')

    # general
    parser.add_argument('--repeat', type=int, default=1,
                        help='How many time to repeat the process. If set to 0 repeat indefinitely [default: %(default)s]')
    parser.add_argument('--sleep', type=float, default=60, help='How many seconds to wait between each iteration')
    parser.add_argument('--print', type=bool, nargs='?', const=True, default=False,
                        help='print content in file instead of sending to MQTT')
    parser.add_argument('--exception', type=bool, nargs='?', const=True, default=False,
                        help='whether to print error messages or not')
    args = parser.parse_args()

    end_time = datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT)
    if args.end_time is not None:
        end_time = args.end_time

    if args.end_time is not None:
        if args.print is True:
            print_content(db_name=args.db_name, start_time=args.start_time, end_time=end_time, system=args.system,
                          location=args.location, component=args.component, data_dir=args.data_dir,
                          exception=args.exception)
        else:
            mqtt_send(topic=args.topic, db_name=args.db_name, broker=args.broker, port=args.port, user=args.user,
                      passwd=args.passwd, mqtt_wait=args.mqtt_wait, start_time=args.start_time, end_time=end_time,
                      system=args.system, location=args.location, component=args.component, data_dir=args.data_dir,
                      exception=args.exception)
    elif args.repeat == 0:
        # repeat indefinitely
        while True:
            if args.print is True:
                print_content(db_name=args.db_name, start_time=args.start_time, end_time=end_time, system=args.system,
                              location=args.location, component=args.component, data_dir=args.data_dir,
                              exception=args.exception)
            else:
                mqtt_send(topic=args.topic, db_name=args.db_name, broker=args.broker, port=args.port, user=args.user,
                          passwd=args.passwd, mqtt_wait=args.mqtt_wait, start_time=args.start_time, end_time=end_time,
                          system=args.system, location=args.location, component=args.component, data_dir=args.data_dir,
                          exception=args.exception)
            time.sleep(args.sleep)
            args.start_time, end_time = __update_timestamps(end_time=end_time)
    elif args.repeat >= 1:
        for i in range(args.repeat):
            if args.print is True:
                print_content(db_name=args.db_name, start_time=args.start_time, end_time=end_time, system=args.system,
                              location=args.location, component=args.component, data_dir=args.data_dir,
                              exception=args.exception)
            else:
                mqtt_send(topic=args.topic, db_name=args.db_name, broker=args.broker, port=args.port, user=args.user,
                          passwd=args.passwd, mqtt_wait=args.mqtt_wait, start_time=args.start_time, end_time=end_time,
                          system=args.system, location=args.location, component=args.component, data_dir=args.data_dir,
                          exception=args.exception)
            time.sleep(args.sleep)
            args.start_time, end_time = __update_timestamps(end_time=end_time)


if __name__ == '__main__':
    main()
