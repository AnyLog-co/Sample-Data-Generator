import ast
import json
import requests
from bs4 import BeautifulSoup
import locale


from source.rest_calls import RestClient
# from rest_calls import  RestClient

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

def read_chunks(file_obj, chunk_size=100):
    chunk = []
    for line in file_obj:
        chunk.append(line)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def declare_policy(client:RestClient, policy:dict):
    headers = {
        "command": "blockchain insert where policy=!new_policy and local=true and master=!ledger_conn",
        "User-Agent": "AnyLog/1.23"
    }


    client.publish_data(headers=headers, payload=f"<new_policy={json.dumps(policy)}>")


def get_policy_id(client:RestClient, policy_type:str, name:str, **kwargs):
    headers = {
        "command": f"blockchain get {policy_type} where name={name}",
        "User-Agent": "AnyLog/1/23"
    }

    if kwargs:
        for key, value in kwargs:
            if value not in ["", None]:
                if " " in value.strip():
                    headers["command"] += f' and {key}="{value.strip}"'
                else:
                    headers["command"] += f' and {key}={value.strip}'

    response = client.get_data(headers)

    return None if response == '[]' else response


def get_files_by_url(url:str)->list:
    """
    Get list of CSV files for Rig data
    :params:
        url:str - RIG files url path
    :return:
        list of files
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a")]
        return [link for link in links if link and  (link.endswith(".csv") or link.endswith(".json"))]
    except Exception as error:
        raise Exception(f"Failed to access data files {url} (Error: {error})")


def read_url_content(url:str, row_id:int=0, encoding:str=None)->dict:
    """
    Read content based on the URL
    :args:
        url:str - URL address
        row_id:int - index to get row
    :return:
        content based on row_id
    """
    raw_content = {}
    content = {}
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        if url.endswith('csv'):
            headers = response.text.split("\n")[0].split(",")
            row = response.text.split("\n")[row_id+1].split(",")
            for index in range(len(headers)):
                raw_content[headers[index]] = row[index]
        elif url.endswith('.json') and encoding:
            locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')  # Linux / Mac
            text = response.content.decode(encoding)
            rows = [json.loads(line) for line in text.splitlines() if line.strip()]
            raw_content = rows[row_id]
    except Exception as error:
        raise Exception(f"Failed to content in {url} (Error: {error})")
    for key, value in raw_content.items():
        try:
            value =  locale.atof(value)
        except Exception:
            pass
        try:
            content[key.strip()] = ast.literal_eval(value)
        except:
            content[key.strip()] = value

    return content
