import ast
import copy
import datetime
import json
import locale
import re


import requests
from bs4 import BeautifulSoup
from source.northbound.rest_calls import get_file_content

def extract_credentials(credentials:str):
    """
    Extract credentials from user input
    :args:
        credentials:str - connection information
            [ip]:[port]
            [user]:[password]@[ip]:[port]
    :params:
        borker:str -  IP
        port:int
        user:str
        password:str
    :return:
        broker, port, user, password
    """
    user = None
    password = None
    broker, port = credentials.split(':')
    if '@' in credentials:
        creds, conn = credentials.split('@')
        user, password = creds.split(':')
        broker, port = conn.split(":")
    try:
        port = int(port)
    except:
        pass

    return broker, port, user, password


def get_files_by_url(url:str)->list:
    """
    Get list of CSV files for Rig data
    :args:
        url:str - RIG files url path
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
            content = [link for link in links if link and (link.endswith(f".{ending}") for ending in ["csv", "json"])]
        except Exception as error:
            raise Exception(f"Failed to access data files {url} (Error: {error})")

    return [fname for fname in content if fname.rsplit('.')[-1] in ext_types]

def read_csv_content(url:str, row_id:int=0)->dict|None:
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

def read_json_content(url:str, row_id:int)->dict|None:
    response = get_file_content(url=url, timeout=30)
    raw_content = {}
    content = None
    if response:
        try:
            raw_content = response.json()[row_id]
        except requests.JSONDecodeError:
            response_content = response.text.splitlines()[row_id]
            if ": {" in response_content.strip() and not response_content.strip().startswith('{'):
                response_content = response_content.split(": ", 1)[-1]
            raw_content = json.loads(response_content.strip())
        except IndexError:
            raw_content = None
    if raw_content:
        content = raw_content
    return content


def read_turbine_data(url:str, row_id:int)->dict|None:
    response = get_file_content(url=url, timeout=30)
    raw_content = {}
    content = None
    if response:
        try:
            locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')  # Linux / Mac
            text = response.content.decode("utf-8-sig")
            rows = [json.loads(line) for line in text.splitlines() if line.strip()]
            raw_content = rows[row_id]
        except IndexError:
            raw_content = None

    if raw_content:
        content = {}
        for key, value in raw_content.items():
            try:
                value = locale.atof(value)
                if key == "Anlage":
                    value = int(value)
            except Exception:
                pass
            try:
                content[key.strip()] = ast.literal_eval(value)
            except:
                content[key.strip()] = value

    return content


def timestamp_calculator(timestamp:datetime.datetime, offset:float, id_index:int):
    try:
        timestamp += datetime.timedelta(seconds=offset*id_index)
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')
    except Exception as error:
        raise Exception(f"Failed to calculate timestamp (Error: {error})")



def _to_snake(name: str) -> str:
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