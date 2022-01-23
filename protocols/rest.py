import requests
import support


def post_data(conn:str, data:list, dbms:str, table:str=None, rest_topic:str='new-topic', auth:tuple=None,
              timeout:int=30, exception:bool=False)->bool:
    """
    Send data via REST using POST command
    :notes:
        URL: https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#using-a-post-command
        Comment: requires MQTT client call on the accepting AnyLog side
    :args:
        conn:str - REST connection information
        data - either a list or dict of data sets
        rest_topic:str - MQTT topic
        dbms:str - logical database name
        table:str - table name, if data is dict use keys as table name(s)
        auth:tuple - Authentication username + password
        timeout:nt - wait time
        exception:bool - whether or not to print error messages
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

    payloads = support.payload_conversions(payloads=data, dbms=dbms, table=table)
    for payload in payloads:
        try:
            r = requests.post(url='http://%s' % conn, headers=headers, data=payload, auth=auth, timeout=timeout)
        except Exception as e:
            if exception is True:
                print('Failed to POST content into %s (Error: %s)' % (conn, e))
            status = False
        else:
            if int(r.status_code) != 200 and exception is True:
                print('Failed to POST content into %s (Network Error: %s)' % (conn, r.status_code))
                status = False
            elif int(r.status_code) != 200:
                status = False

    return status


def put_data(conn:str, data:list, dbms:str, table:str=None, auth:tuple=None, timeout:int=30, exception:bool=False)->bool:
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
        exception:bool - whether or not to print error messages
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
        headers['table'] = table
        for row in data:
            try:
                r = requests.put(url='http://%s' % conn, headers=headers, data=support.json_dumps(row), auth=auth, timeout=timeout)
            except Exception as e:
                if exception is True:
                    print('Failed to PUT data into %s (Error: %s)' % (conn, e))
                status = False
            else:
                if int(r.status_code) != 200 and exception is True:
                    print('Failed to PUST data into %s (Network Error: %s)' % r.status_code)
                    status = False
                elif int(r.status_code) != 200:
                    status = False

    elif isinstance(data, dict):
        for table in data:
            headers['table'] = table
            for row in data[table]:
                try:
                    r = requests.put(url='http://%s' % conn, headers=headers, data=support.json_dumps(row), auth=auth, timeout=timeout)
                except Exception as e:
                    if exception is True:
                        print('Failed to PUT data into %s (Error: %s)' % (conn, e))
                    status = False
                else:
                    if int(r.status_code) != 200 and exception is True:
                        print('Failed to PUST data into %s (Network Error: %s)' % r.status_code)
                        status = False
                    elif int(r.status_code) != 200:
                        status = False
    return status





