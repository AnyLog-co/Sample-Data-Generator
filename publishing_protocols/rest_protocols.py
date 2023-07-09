import json
import requests
import support
import time

NETWORK_ERRORS_GENERIC = {
    1: "Informational",
    2: "Successful",
    3: "Redirection",
    4: "Client Error",
    5: "Server Error",
    7: "Developer Error"
}
NETWORK_ERRORS = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    426: "Upgrade Required",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Time-out",
    505: "HTTP Version Not Supported",
    102: "Processing",
    207: "Multi-Status",
    226: "IM Used",
    308: "Permanent Redirect",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    511: "Network Authentication Required"
}


def __convert_data(payloads:list)->dict:
    """
    Extract logical database name and table name from payload
    :args:
        payloads:list - content to PUT
    :params:
        content:dict - formatted payloads
    """
    content = {}

    if isinstance(payloads, list):
        for payload in payloads:
            if isinstance(payload, list):
                content = __convert_data(payloads=payload)
            else:
                name = payload['dbms'] + "." + payload['table']
                del payload['dbms']
                del payload['table']
                if name not in content:
                    content[name] = []
                content[name].append(payload)
    else:
        name = payloads['dbms'] + "." + payloads['table']
        del payloads['dbms']
        del payloads['table']
        if name not in content:
            content[name] = []
        content[name].append(payloads)

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
            r = requests.put(url=f'http://{conn}', headers=headers, auth=auth, timeout=timeout, data=payload)
        except Exception as error:
            status = False
            if exception is True:
                print(f'Failed to execute PUT for {table} against {conn} (Error: {error})')
        else:
            status_code = int(r.status_code)
            if status_code != 200:
                status = False
                if exception is True:
                    error_msg = f"Failed to execute PUT for {table} against {conn} (Network Error: {status_code} - %s)"
                    if status_code in NETWORK_ERRORS:
                        error_msg = error_msg % NETWORK_ERRORS[status_code]
                    elif int(str(status_code)[0]) in NETWORK_ERRORS_GENERIC:
                        error_msg = error_msg % NETWORK_ERRORS_GENERIC[int(str(status_code)[0])]
                    else:
                        error_msg.replace(" %s)", ")")
                    print(error_msg)

    time.sleep(10)
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

    str_payloads = json.dumps(payloads)
    try:
        r = requests.post(url=f"http://{conn}", headers=headers, auth=auth, timeout=timeout, data=str_payloads)
    except Exception as error:
        status = False
        if exception is True:
            print(f'Failed to execute POST against {conn} (Error: {error})')
        exit(1)
    else:
        if int(r.status_code) != 200:
            status = False
            status_code = int(r.status_code)
            if status_code != 200:
                status = False
                if exception is True:
                    error_msg = f"Failed to execute POST against {conn} (Network Error: {status_code} - %s)"
                    if status_code in NETWORK_ERRORS:
                        error_msg = error_msg % NETWORK_ERRORS[status_code]
                    elif int(str(status_code)[0]) in NETWORK_ERRORS_GENERIC:
                        error_msg = error_msg % NETWORK_ERRORS_GENERIC[int(str(status_code)[0])]
                    else:
                        error_msg.replace(" %s)", ")")
                    print(error_msg)

    return status






