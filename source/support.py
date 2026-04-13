import os
import copy
import datetime
import json
import re

from bs4 import BeautifulSoup
from source.northbound.rest_calls import RestClient

TIMESTAMP_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}):\s*(.*)")

# ====== Basic support functions ======

def find_closest_row(index, target_ts):
    # index = list[(timestamp, row_id)]
    if isinstance(target_ts, str):
        try:
            target_ts = datetime.datetime.strptime(target_ts, "%Y-%m-%d %H:%M:%S")
        except Exception as error:
            raise Exception(f"Failed to convert {target_ts} to proper format: '%Y-%m-%d %H:%M:%S' (Error: {error}")
    elif not isinstance(target_ts, datetime.datetime):
        raise Exception(f"Failed to convert {target_ts} to proper format: '%Y-%m-%d %H:%M:%S'")

    best = None
    best_diff = None

    for ts, row_id in index:
        diff = abs((ts - target_ts).total_seconds())
        if best_diff is None or diff < best_diff:
            best = row_id
            best_diff = diff

    return best

def to_snake(name: str)->str:
    """
    Convert camelCase or PascalCase to snake_case.
    Examples:
        timeBattery -> time_battery
        maxBatteryPower -> max_battery_power
        TimeBattery -> time_battery
    """
    # Insert underscore before capital letters, except at the start
    s = re.sub(r'(?<!^)([A-Z])', r'_\1', name)
    return s.lower()

def extract_credentials(credentials:str):
    """
    Extract credentials from user input
    :args:
        credentials:str - connection information
            [ip]:[port]
            [user]:[password]@[ip]:[port]
    :params:
        broker:str -  IP
        port:int - port associated with IP
        user:str - user used for security
        password:str - password associated with user
    :return:
        broker, port, user, password
    """
    user = None
    password = None
    if '@' in credentials:
        creds, conn = credentials.split('@')
        user, password = creds.split(':')
        broker, port = conn.split(":")
    else:
        broker, port = credentials.split(':')
    try:
        port = int(port)
    except:
        pass

    return broker, port, user, password

# ====== Data File processing ======
def _decouple_vessel_data_format(match:re.match)->dict:
    """
    If data is in the following format (used with vessels) then to the correct format
    :sample format:
        2026-01-01 00:00:00: '{"column1": .... }'
    :args:
        match - broken up string
    :params:
        timestamp:str - timestamp
        json_part:str - json
    :return:
        if all is correct then dict (from json_part) that includes timestamp
        else raises Exception
    """
    timestamp = match.group(1)  # "2024-08-15 00:13:59"
    json_part = match.group(2)  # '{"batteryErrorCode": 0,is ...'

    try:
        content = json.loads(match.group(2)) if  not isinstance(match.group(2), dict) else match.group(2)
        content["timestamp"] = timestamp
    except Exception as error:
        raise Exception(f"Invalid content extracted from file - {timestamp}: {json_part} (Error: {error})")

    return content

def _parse_german_number(value)->str|float|int:
    """
    For German format data, convert str to proper numeric type
    :args:
        value - content to convert if not string
    :return:
        updated value
    """
    if not isinstance(value, str):
        return value
    value = value.strip()

    if ',' in value and '.' in value:
        value = value.replace('.', '').replace(',', '.')
    elif ',' in value:
        value = value.replace(',', '.')

    try:
        return ast.literal_eval(value)
    except Exception:
        return value


def _decouple_german_content(content):
    if isinstance(content, str):
        content = json.loads(content.strip())
    return {
        key.strip(): _parse_german_number(value) for key, value in content.items()
    }

def _decouple_content(row, is_german:bool=False):
    output = row
    if isinstance(row, str) and (match := TIMESTAMP_RE.match(row)):
        output = _decouple_vessel_data_format(match)
    elif is_german:
        output = _decouple_german_content(content=row)
    elif isinstance(row, str):
        try:
            output = json.loads(row)
        except Exception as error:
            raise Exception(f"Failed to parse content from {url} (Error: {error})")

    if isinstance(output, list):
        return [
            _decouple_content(orow) for orow in output
        ]

    return output

def get_files_by_url(url):
    """
    Given a URL address - extract list of files under it.
    Think of it like an `ls` command against the URL
    """
    client = RestClient(conn=url, auth=None, timeout=120)
    raw_response = client.get_data(headers=None, raw_response=True)
    toc_content = []
    if 200 <= int(raw_response.status_code) < 300:
        try:
            soup = BeautifulSoup(raw_response.text, "html.parser")
            links = [a.get("href") for a in soup.find_all("a")]
            content = [link for link in links if link and (link.endswith(f".{ending}") for ending in ["csv", "json"])]
        except Exception as error:
            raise Exception(f"Failed to access data files {url} (Error: {error})")
        else:
            toc_content = [fname for fname in content if fname.rsplit('.')[-1] in ["csv", "json"]]
    return toc_content

def url_read_content(url:str, line:int|None=None, is_german:bool=False):
    file_name = os.path.basename(url)
    client = RestClient(conn=url, auth=None, timeout=120)
    content = client.get_file_data(line_num=line+1, is_german=is_german, is_csv=file_name.endswith("csv"))

    return _decouple_content(content, is_german=is_german)

def url_read_content_full(url:str):
    """
    Extract ful content from file
    """
    client = RestClient(conn=url, auth=None, timeout=120)
    content = client.get_data(headers=None, raw_response=any(url.endswith(ext) for ext in ["json", "csv"]))
    return content

def read_json_file(file_path:str):
    """
    Read JSON file into memory
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as error:
        raise Exception(f"Failed to read content in {file_path} (Error: {error})")


# ====== Mapping code ======

def mapping_param(content:list):
    data_type = "string"
    if str in content:
        data_type = "string"
    elif bool in content:
        data_type = "bool"
    elif float in content:
        data_type = "float"
    elif int in content:
        data_type = "int"
    return data_type

def mapping_policy_config(content:dict, function=None)->dict:
    schema = {}
    for key in content:
        value = copy.deepcopy(key)
        if function:
            key = function(key)
        if key != "timestamp":
            if str in content.get(value):
                schema[key] = {
                    "type": "string",
                    "default": "",
                    "bring": f"[{value}]"
                }
            elif bool in content.get(value):
                schema[key] = {
                    "type": "bool",
                    "default": "",
                    "bring": f"[{value}]"
                }
            elif float in content.get(value):
                schema[key] = {
                    "type": "float",
                    "bring": f"[{value}]"
                }
            elif int in content.get(value):
                schema[key] = {
                    "type": "int",
                    "bring": f"[{value}]"
                }
            else:
                schema[key] = {
                    "type": "string",
                    "default": "",
                    "bring": f"[{value}]"
                }
    return schema


if __name__ == "__main__":
    get_files_by_url("http://45.33.11.32/Sample-Data/vessel-data/")
    # url_read_content_full("http://45.33.11.32/Sample-Data/vessel-data/2024-08-15_Helios_DLB_BMWix_IP_3_ID_33.json")