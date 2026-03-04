import ast
import copy
import datetime
import json
import locale
import re

import requests
from bs4 import BeautifulSoup
from source.northbound.rest_functions import get_file_content

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

def get_files_by_url(url:str)->list:
    """
    Get list of files based on a URL
    :args:
        url:str - URL with files
    :params:
        ext_types:list - list of extension type(s) - currently supporting CSV and JSON
    :return:
        list of files
    """
    ext_types = ["csv", "json"]

    response = get_file_content(url=url, timeout=30)
    content = None
    if response:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a.get("href") for a in soup.find_all("a")]
            content = [link for link in links if link and (link.endswith(f".{ending}") for ending in ext_types)]
        except Exception as error:
            raise Exception(f"Failed to access data files {url} (Error: {error})")

    return [fname for fname in content if fname.rsplit('.')[-1] in ext_types]

def read_csv_content(url:str, row_id:int=0)->dict|None:
    """
    Read content from CSV file
    :args:
        url:str - RIG files url path
        row_id:int - row number to extract content from
    :params:
        response:response.Requests - raw request response
        raw_content:dict - raw content from request
        content:str|None - actual content to store
    :return:
        content
    """
    response = get_file_content(url=url, timeout=30)
    raw_content = {}
    content = None
    if response:
        try:
            headers = response.text.split("\n")[0].split(",")
            row = response.text.split("\n")[row_id + 1].split(",")
            for index in range(len(headers)):
                raw_content[headers[index]] = row[index]
        except IndexError:
            raw_content = None
    if raw_content:
        content = {}
        for key, value in raw_content.items():
            try:
                content[key.strip()] = ast.literal_eval(value)
            except:
                content[key.strip()] = value
            if key == "timestamp":
                content[key.strip()] = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

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


def _german_content(content, row_id:int|None=None):
    try:
        text = content.content.decode("utf-8-sig")
    except Exception as error:
        # raise  Exception(f"Failed to parse content from wind-turbine / German (Error: {error})")
        return None

    if row_id is None or len(text.splitlines()) <= row_id:
        return None

    raw_content = text.splitlines()[row_id].strip()
    raw_content = json.loads(raw_content)
    return {
        key.strip(): _parse_german_number(value)
        for key, value in raw_content.items()
    }


def _standard_json_content(content, row_id:int|None=None, timestamp:str|datetime.datetime|None=None):
    try:
        data = content.json()
        if row_id is not None:
            return data[row_id]
        return data

    except requests.JSONDecodeError:
        # fallback to line-based JSON
        lines = content.text.splitlines()

        if timestamp is not None:
            for line in lines:
                if str(timestamp) in line:
                    return json.loads(line.strip())

        if row_id is not None and row_id < len(lines):
            line = lines[row_id].strip()
            if line and ": {" in line and not line.startswith("{"):
                timestamp, line = line.split(": ", 1)
                timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            return timestamp, json.loads(line.strip())

        return None


def read_json_content(url:str, row_id:int|None=None, timestamp:str|datetime.datetime|None=None, german_format:bool=False, timeout:float=30)->(dict|None) or (dict|None, str):
    line = None
    response = get_file_content(url=url, timeout=timeout)
    if not response:
        return None
    elif german_format:
        return _german_content(content=response, row_id=row_id)
    else:
        return _standard_json_content(content=response, row_id=row_id, timestamp=timestamp)



# def read_json_content(url:str, row_id:int|None=None, timestamp:str|datetime.datetime|None=None, german_format:bool=False, timeout:float=30)->(dict|None) or (dict|None, str):
#     """
#     Read content from a given (URL) file
#     :args:
#         url:str - URL with files
#         row_id:int|None - row number to extract content from
#         timestamp:str|None=None - timestamp for row
#         german_format:bool - whether data is German format
#         timeout:float - REST timeout
#     :params:
#         response:response.Requests - raw request response
#         raw_content:dict - raw content from request
#         content:str|None - actual content to store
#     :return:
#         content
#     """
#     line = None
#     response = get_file_content(url=url, timeout=timeout)
#     is_split = False
#     if not response:
#         return None
#
#     try:
#         if german_format:
#             # Line-by-line JSON (wind turbine format)
#             locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
#             text = response.content.decode("utf-8-sig")
#             rows = [json.loads(line) for line in text.splitlines() if line.strip()]
#             if row_id:
#                 raw_content = rows[row_id]
#         else:
#             # Standard JSON array
#             try:
#                 raw_content = response.json()[row_id]
#             except requests.JSONDecodeError:
#                 # Fallback to line-based parsing
#
#                 line = None
#                 if timestamp is not None:
#                     line = None
#                     lines = response.text.splitlines()
#                     for read_lines in lines:
#                         if timestamp in read_lines:
#                             line = read_lines
#                             break
#
#                 if not line:
#                     line = response.text.splitlines()[row_id]
#                 if line and ": {" in line.strip() and not line.strip().startswith("{"):
#                     is_split = True
#                     timestamp, line = line.split(": ", 1)
#                     try: # convert timestamp to datetime
#                         timestamp = datetime.datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
#                     except Exception as error:
#                         pass
#                 if line is None:
#                     print(url)
#                     exit(1)
#                 else:
#                     raw_content = json.loads(line.strip())
#     except (IndexError, ValueError, json.JSONDecodeError):
#         return None
#
#     if not german_format and not is_split:
#         return raw_content
#     elif not german_format:
#         return timestamp, raw_content
#
#     # German numeric normalization
#     content = {}
#     for key, value in raw_content.items():
#         try:
#             value = locale.atof(value)
#             if key == "Anlage":
#                 value = int(value)
#         except Exception:
#             pass
#
#         try:
#             content[key.strip()] = ast.literal_eval(value)
#         except Exception:
#             content[key.strip()] = value
#
#     return content

def read_json_file(file_path:str):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as error:
        raise Exception(f"Failed to read content in {file_path} (Error: {error})")

def timestamp_calculator(timestamp:datetime.datetime, offset:float, id_index:int)->str:
    """
    Calculate new timestamp based on base-timestamp
    :args:
        timestamp:datetime.datetime - base timestamp
        id_index:int - row ID
        offset:float - time offset if  "topic ID" changes
    :return:
        updated timestamp based on id_index and offset
    """
    try:
        timestamp += datetime.timedelta(seconds=offset*id_index)
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')
    except Exception as error:
        raise Exception(f"Failed to calculate timestamp (Error: {error})")


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