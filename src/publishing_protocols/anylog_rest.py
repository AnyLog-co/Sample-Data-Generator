import random
import requests
import json

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

class AnyLogREST:
    def __init__(self, conns:str, timeout:float, topic:str, exception:bool=False):
        """
        Anylog REST class
        :args:
            conns:str - user inputted connection information
            timeout:float - REST timeout
            topic:str - REST POST / MQTT topic
            exception:bool - whether to print exceptions
        :self:
            self.conns:dict - connection information
            self.timeout:float - REST timeout
            self.topic:str - REST POST / MQTT topic
            self.exception:bool - whether to print exceptions
        """
        self.timeout = timeout
        self.topic = topic
        self.exception = exception

        self.conns = {}
        for conn in conns.split(","):
            if '@' not in conn:
                self.conns[conn] = ()
            else:
                self.conns[conn.split("@")[0]] = tuple(conn.split("@")[-1].split(":"))

    def get_data(self, headers:dict):
        """
        Execute GET command based on headers
        :args:
            headers:dict - REST  headers
        """
        output = None
        conn = random.choice(list(self.conns))
        try:
            r = requests.get(url=f"http://{conn}", headers=headers, auth=self.conns[conn], timeout=self.timeout)
        except Exception as error:
            if self.exception is True:
                print(f"Failed to execute GET information for {headers['command']} against {conn} (Error: {error})")
        else:
            status_code = int(r.status_code)
            if status_code != 200:
                if self.exception is True:
                    error_msg = f"Failed to execute command {headers['command']} against {conn} (Network Error: {status_code} - %s)"
                    if status_code in NETWORK_ERRORS:
                        error_msg = error_msg % NETWORK_ERRORS[status_code]
                    elif int(str(status_code)[0]) in NETWORK_ERRORS_GENERIC:
                        error_msg = error_msg % NETWORK_ERRORS_GENERIC[int(str(status_code)[0])]
                    else:
                        error_msg.replace(" %s)", ")")
                    print(error_msg)
            else:
                try:
                    output = r.json()
                except:
                    output = r.text

        return output

    def put_data(self, payloads:list):
        """
        Execute REST PUT
        :args:
            payloads:list - content to store in AnyLog
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
        conn = random.choice(list(self.conns))
        headers = {
            "type": "json",
            "dbms": None,
            "table": None,
            "mode": "streaming",
            "User-Agent": "AnyLog/1.23",
            "Content-Type": "text/plain"
        }

        headers['dbms'] = payloads[0]['dbname']
        headers['table'] = payloads[0]['table']

        for payload in payloads:
            del payload['dbms']
            del payload['table']

        try:
            r = requests.put(url=f"http://{conn}", data=json.dumps(payloads), headers=headers, auth=self.conns[conn],
                             timeout=self.timeout)
        except Exception as error:
            if self.exception is True:
                print(f"Failed to execute PUT against {conn} (Error: {error})")
        else:
            status_code = int(r.status_code)
            if status_code != 200:
                status = False
                if self.exception is True:
                    error_msg = f"Failed to execute PUT against {conn} (Network Error: {status_code} - %s)"
                    if status_code in NETWORK_ERRORS:
                        error_msg = error_msg % NETWORK_ERRORS[status_code]
                    elif int(str(status_code)[0]) in NETWORK_ERRORS_GENERIC:
                        error_msg = error_msg % NETWORK_ERRORS_GENERIC[int(str(status_code)[0])]
                    else:
                        error_msg.replace(" %s)", ")")
                    print(error_msg)

        return status


    def post_data(self, payloads:list, topic:str):
        """
        Execute REST PUT
        :args:
            payloads:list - content to store in AnyLog
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
        conn = random.choice(list(self.conns))
        headers = {
            'command': 'data',
            'topic': topic,
            'User-Agent': 'AnyLog/1.23',
            'Content-Type': 'text/plain'
        }

        try:
            r = requests.post(url=f"http://{conn}", data=json.dumps(payloads), headers=headers, auth=self.conns[conn],
                             timeout=self.timeout)
        except Exception as error:
            if self.exception is True:
                print(f"Failed to execute PUT against {conn} (Error: {error})")
        else:
            status_code = int(r.status_code)
            if status_code != 200:
                status = False
                if self.exception is True:
                    error_msg = f"Failed to execute PUT against {conn} (Network Error: {status_code} - %s)"
                    if status_code in NETWORK_ERRORS:
                        error_msg = error_msg % NETWORK_ERRORS[status_code]
                    elif int(str(status_code)[0]) in NETWORK_ERRORS_GENERIC:
                        error_msg = error_msg % NETWORK_ERRORS_GENERIC[int(str(status_code)[0])]
                    else:
                        error_msg.replace(" %s)", ")")
                    print(error_msg)

        return status

