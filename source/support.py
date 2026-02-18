import ast
import datetime
import json
import locale

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
    :params:
        url:str - RIG files url path
    :return:
        list of files
    """
    response = get_file_content(url=url, timeout=30)
    content = None
    if response:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a.get("href") for a in soup.find_all("a")]
            content = [link for link in links if link and  (link.endswith(".csv") or link.endswith(".json"))]
        except Exception as error:
            raise Exception(f"Failed to access data files {url} (Error: {error})")
    return content

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
            except Exception:
                pass
            try:
                content[key.strip()] = ast.literal_eval(value)
            except:
                content[key.strip()] = value

    return content



