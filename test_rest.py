import ast
import copy
import json
import os
import re

from source.northbound.rest_calls import RestClient


TIMESTAMP_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}):\s*(.*)")

def __format_1_extraction(match:re.match)->dict:
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


def __decouple_german_content(content):
    if isinstance(content, str):
        content = json.loads(content.strip())
    return {
        key.strip(): _parse_german_number(value) for key, value in content.items()
    }


def __decouple_content(row, is_german:bool=False):
    output = row
    if isinstance(row, str) and (match := TIMESTAMP_RE.match(row)):
        output = __format_1_extraction(match)
    elif is_german:
        output = __decouple_german_content(content=row)
    elif isinstance(row, str):
        try:
            output = json.loads(row)
        except Exception as error:
            raise Exception(f"Failed to parse content from {url} (Error: {error})")

    if isinstance(output, list):
        return [
            __decouple_content(orow) for orow in output
        ]

    return output

def url_read_content(url:str, line:int|None=None, is_german:bool=False):
    file_name = os.path.basename(url)
    client = RestClient(conn=url, auth=None, timeout=120)
    content = client.get_file_data(line_num=line, is_german=is_german, is_csv=file_name.endswith("csv"))

    return __decouple_content(content, is_german=is_german)


if __name__ == "__main__":
    # Proveit
    print("proveit")
    content = url_read_content(url="http://45.33.11.32/Sample-Data/proveit-data2/Enterprise_A.Dallas.Line_1.1.json", line=17)
    print(content)

    # vessel
    print("vessel")
    content = url_read_content(url="http://45.33.11.32/Sample-Data/vessel-data/2024-08-15_Helios_DLB_BMWix_IP_3_ID_33.json", line=3)
    print(content)

    # german (wind turbine)
    print("wind turbine")
    content = url_read_content(url="http://45.33.11.32/Sample-Data/wind-turbine/wind_turbine_5.json", line=5, is_german=True)
    print(content)

    # csv
    print("csv")
    content = url_read_content(url="http://45.33.11.32/Sample-Data/rig-data/drilling_data_RIG-GOM-023.csv", line=5)
    print(content)