import json
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
