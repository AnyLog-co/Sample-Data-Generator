import os
import random
import re
import time

import sample_data_generator.data_generators.kubearmor_syslog as kubearmor_syslog
from sample_data_generator.support.timestamp_generator import generate_timestamp

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)).split("src")[0]
SYSLOG_FILE = os.path.join(ROOT_PATH, 'data', 'syslogs')
PATTERN = re.compile(r'(?P<month>\w{3})\s+(?P<day>\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<hostname>\S+) kernel: \[.*\] \[UFW BLOCK\] (?P<info>.*)')

HOSTNAMES = kubearmor_syslog.SAMPLE_DATA['Hostname']

def __read_logs(exception:bool=False):
    output = None
    try:
        with open(SYSLOG_FILE, 'r') as f:
            try:
                output = [value for value in f.read().split("\n") if value != ""]
            except Exception as error:
                if exception is True:
                    print(f"Failed to read content from syslogs (Error: {error})")
    except Exception as error:
        if exception is True:
            print(f"Failed to open syslogs (Error: {error})")
    return output


def __extract_read_logs(line:str):
    match_line = PATTERN.match(line)
    if match_line:
        return match_line.groupdict()
    return {}

def __create_payload(dbname, line:str, timezone:str, timezone_range:bool=False):
    payload = {
        "dbname": dbname,
        "table": "syslogs",
        "timestamp": generate_timestamp(timezone=timezone, enable_timezone_range=timezone_range),
        'hostname': random.choice(HOSTNAMES)
    }
    line_split = line.split()
    for row in line_split:
        payload[row.strip().split('=', 1)[0]] = row.strip().split('=', 1)[-1]

    return payload


def get_syslogs(dbname:str, row_count:int, sleep:float, timezone:str, timezone_range:bool=False, exception:bool=False):
    payloads = []
    logs = __read_logs(exception=exception)
    for i in range(row_count):
        dict_log = __extract_read_logs(line=random.choice(logs))
        if dict_log != {}:
            payloads.append(__create_payload(dbname=dbname, line=dict_log['info'], timezone=timezone, timezone_range=timezone_range))
            time.sleep(sleep)

    return payloads

