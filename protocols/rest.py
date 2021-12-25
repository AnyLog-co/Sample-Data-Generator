import requests
import convert_json


def post_data(conn:str, data:list, dbms:str, table:str=None, rest_topic:str='new-topic', auth:tuple=None, timeout:int=30)->bool:
    """
    Send data via REST using POST command
    :notes:
        URL: https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#using-a-post-command
        Comment: requires MQTT client call on the accepting AnyLog sidee
    :args:
        conn:str - REST connection information
        data - either a list or dict of data sets
        rest_topic:str - MQTT topic
        dbms:str - logical database name
        table:str - table name, if data is dict use keys as table name(s)
        auth:tuple - Authentication username + password
        timeout:nt - wait time
    :params:
        status:bool
        headers:dict - REST header info
        payloads:list - content to POST
    :return:
        status
    """
    status = True
    headers = {
        'command': 'data',
        'topic': rest_topic,
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }

    payloads = []
    if isinstance(data, list):
        for row in data:
            row['dbms'] = dbms
            row['table'] = table
            payloads.append(convert_json.json_dumps(row))
    elif isinstance(data, dict):
        for table in data:
            for row in data[table]:
                row['dbms'] = dbms
                row['table'] = table
                payloads.append(convert_json.json_dumps(row))

    try:
        r = requests.post(url='http://%s' % conn, headers=headers, data=payloads, auth=auth, timeout=timeout)
    except Exception as e:
        status = False
    else:
        if int(r.status_code) != 200:
            status = Fasle

    return status


def put_data(conn:str, data:list, dbms:str, table:str=None, auth:tuple=None, timeout:int=30)->bool:
    """
    Send data via REST using PUT command
    :url:
        https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#using-a-put-command
    :args:
        conn:str - REST connection information
        data - either a list or dict of data sets
        dbms:str - logical database name
        table:str - table name, if data is dict use keys as table name(s)
        auth:tuple - Authentication username + password
        timeout:nt - wait time
    :params:
        status:bool
        headers:dict - REST header info
        payloads:list - content to POST
    :return:
        status
    """
    status = True
    headers = {
        'type': 'json',
        'dbms': dbms,
        'mode': 'streaming',
        'Content-Type': 'text/plain'
    }

    if isinstance(data, list):
        payloads = []
        headers['table'] = table
        for row in data:
            payloads.append(convert_json.json_dumps(row))
        try:
            r = requests.put(url='http://%s' % conn, headers=headers, data=payloads)
        except Exception as e:
            status = False
        else:
            if int(r.status_code) != 200:
                status = False
    elif isinstance(data, dict):
        for table in data:
            payloads = []
            headers['table'] = table
            for row in data[table]:
                payloads.append(convert_json.json_dumps(row))
            try:
                r = requests.put(url='http://%s' % conn, headers=headers, data=payloads, auth=auth, timeout=timeout)
            except Exception as e:
                status = False
            else:
                if int(r.status_code) != 200:
                    status = False

    return status





