import requests
import support

def __convert_data(payloads:list)->dict:
    """
    Extract logical database name and table name from payload
    :args:
        payloads:list - content to PUT
    :params:
        content:dict - formmatted payloads
    """
    content = {}

    for payload in payloads:
        name = f"{payload['dbms'].payload[table]}"
        del payload['dbms']
        del payload['name']
        if name not in content:
            content[name] = []
        content[name].append(payload)

    return content


def put_data(payloads:list, conn:str, auth:tuple=(), timeout:int=30, exception:bool=False):
    """
    Execute REST PUT
    :args:
        payloads:list - content to store in AnyLog
        conn:str - REST IP + Port information
        auth:tuple - authentication information
        timeout:int - REST timeout
        exception:bool - whether to write  exceptions or not
    :params:
        status:bool
        headers:dict - REST header information
        r:requests.Request - result from PUT request
        formatted_payloads:dict - formatting of payloads
        payload:str - JSON dict of payloads
    :return:
        status
    """
    status = True
    headers = {
        'type': 'json',
        'dbms': None,
        'table': None,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    formatted_payloads = __convert_data(payloads=payloads)
    for table in formatted_payloads:
        headers['dbms'], headers['table'] = table.split('.')
        payload = support.json_dumps(payloads=formatted_payloads[table])
        try:
            r = requests.put(url=f'http://{conn}', headers=headers, auth=auth, timeout=timeout)
        except Exception as error:
            status = False
            if exception is True:
                print(f'Failed to execute PUT for {table} against {conn} (Error: {error})')
        else:
            if int(r.status_code) != 200:
                status = False
                if exception is True:
                    print(f'Failed to execute PUT for {table} against {conn} (Network Error: {r.status_code})')

    return status


def post_data(payloads:list, conn:str, topic:str="demo", auth:tuple=(), timeout:int=30, exception:bool=False):
    """
    Execute REST POST
    :args:
        payloads:list - content to store in AnyLog
        conn:str - REST IP + Port information
        topic:str- topic to correlate with the incoming data
        auth:tuple - authentication information
        timeout:int - REST timeout
        exception:bool - whether to write  exceptions or not
    :params:
        status:bool
        headers:dict - REST header information
        str_payloads:str - JSON string of payloads
        r:requests.Request - result from PUT request
    """
    status = True
    headers = {
        'command': 'data',
        'topic': topic,
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }

    str_payloads = support.json_dumps(payloads=payloads)

    try:
        r = requests.post(url=f'https://{conn}', headers=headers, auth=auth, timeout=timeout, data=str_payloads)
    except Exception as error:
        status = False
        if exception is True:
            print(f'Failed to execute POST against {conn} (Error: {error})')
    else:
        if int(r.status_code) != 200:
            status = False
            if exception is True:
                print(f'Failed to execute POST against {conn} (Network Error: {r.status_code})')

    return status






