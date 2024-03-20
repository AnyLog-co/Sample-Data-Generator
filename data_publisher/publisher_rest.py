import requests
from data_generator.support import serialize_data

def publish_via_put(conn:str, payload:list, auth:tuple=(), timeout:float=30, exception:bool=False):
    status = True
    headers = {
        'type': 'json',
        'dbms': None,
        'table': None,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    if isinstance(payload, list):
        headers['dbms'] = payload[0]['dbms']
        headers['table'] = payload[0]['table']
        for row in payload:
            del row['dbms']
            del row['table']
    elif isinstance(payload, dict):
        headers['dbms'] = payload['dbms']
        headers['table'] = payload['table']
        del payload['dbms']
        del payload['table']

    try:
        r = requests.put(url=f'http://{conn}', headers=headers, data=serialize_data(payload=payload), auth=auth, timeout=timeout)
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to execute PUT against {conn} (Error: {error})")
    else:
        status = str(r.status_code).startswith('2')
        if  status is False and exception is True:
            print(f"Failed to execute PUT against {conn} (Network Error: {r.status_code})")
    return status


def publish_via_post(conn:str, payload:list, topic:str, auth:tuple=(), timeout:float=30, exception:bool=False):
    status = True
    headers = {
        'command': 'data',
        'topic': topic,
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.post(url=f'http://{conn}', headers=headers, data=serialize_data(payload=payload), auth=auth, timeout=timeout)
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to execute PUT against {conn} (Error: {error})")
    else:
        status = str(r.status_code).startswith('2')
        if  status is False and exception is True:
            print(f"Failed to execute PUT against {conn} (Network Error: {r.status_code})")
    return status
