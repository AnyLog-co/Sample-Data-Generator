import json
import requests
from source.northbound.error_codes import REST_EXCEPTION_CODES
from source.northbound.error_codes import HTTP_STATUS_CODES
from source.northbound.error_codes import REQUEST_EXCEPTION_MAP


class RestClient:
    def __init__(self, conn:str, auth:tuple=None, timeout:float=60):
        """
        Class to support cURL requests against the network
        :args:
            conn:str - base for URL
        :params:
            self.url - full connection path
            self.timeout:float - REST timeout
            self.auth:tuple - authentication infomration
        """
        self.url = f"http://{conn}" if not conn.startswith("http") else conn
        self.timeout = timeout
        self.auth = auth

    def _execute_command(self, method:str, headers:dict, payload=None)->requests.Request:
        """
        Execute cURL command against the URL
        :args:
            method:str - method to execute (PUT, POST, GET)
            headers:dict - REST headers
            payload:Any - content to publish into AnyLog / EdgeLake
        :param:
            response:requests.Requests - REST request response
        :raise:
            raise exception if fails, using the exception coes in `error_code.py`
        :return:
            response if successful
        """
        if (isinstance(payload, list) and isinstance(payload[0], dict)) or isinstance(payload, dict):
            payload = json.dumps(payload)
        try:
            response = requests.request(method=method.upper(), url=self.url, headers=headers, auth=self.auth,
                                        timeout=self.timeout, data=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code
            status_msg = HTTP_STATUS_CODES.get(status_code)
            if not status_msg:
                # fallback to first-digit mapping to REST_EXCEPTION_CODES
                first_digit = int(str(status_code)[0])
                status_msg = REST_EXCEPTION_CODES.get(first_digit, "Unknown REST error")

            error_msg = (
                f"Failed to execute {method.upper()} against {self.url} "
                f"(Network Error {status_code}: {status_msg} | Response: {error.response.text})"
            )
            raise requests.exceptions.HTTPError(error_msg, response=error.response) from error

        except Exception as error:
            # Any transport/network errors (ConnectionError, Timeout, etc.)
            error_type = type(error).__name__
            error_code = REQUEST_EXCEPTION_MAP.get(error_type, 899)
            error_msg = REST_EXCEPTION_CODES.get(error_code, str(error))

            raise Exception(
                f"Failed to execute {method.upper()} against {self.url} "
                f"(Transport Error {error_code}: {error_msg})"
            ) from error

        return response

    def publish_data(self, headers:dict, payload, method:str="POST"):
        """
        Execute REST POST / PUT command to publish data against AnyLog / EdgeLake
        :args:
            headers:dict - REST headers
            payload: Any - content to publish into AnyLog / EdgeLake
            method:dict - format to publish data (PUT or POST)
        :return:
            response from   `_execute_command`
        """
        return self._execute_command(method=method.upper(), headers=headers, payload=payload)

    def get_data(self, headers:dict|None=None, raw_response:bool=False):
        """
        Execute REST GET command to get data from AnyLog / EdgeLake
        :args:
            headers:dict - REST headers
            raw_response:bool - return raw response rather than extract data
        :return:
            if raw_response - return response
            else - try to parse in JSON if fails return text format
        """
        response = self._execute_command(method="GET", headers=headers)
        if raw_response:
            return response

        try:
            return response.json()
        except Exception:
            return response.text





def declare_mapping_policy(conn:RestClient, policy:dict, **kwargs)->str|None:
    #--- To review ---#
    """
    Check whether a policy exists and if not declare policy and extract policy ID
    can be used for
        - mapping
        - uns
    :args:
        conn:RestClient - connection to REST
        policy:dict - Policy to publish
        kwargs:dict - arguments for WHERE when checking if policy exists
    :params:
        policy_id:str - extract policy ID if exists
    """
    try:
        policy_id = policy.get("mapping").get("id")
    except AttributeError:
        policy_id = None

    get_headers = {
        "command": f"blockchain get *",
        "User-Agent": "AnyLog/1.23"
    }

    if policy_id or kwargs:
        get_headers["command"] += " where "
        if policy_id and "id" not in list(kwargs.values()):
            get_headers["command"] += f' id="{policy_id}" and '
        for name, var in kwargs.items():
            get_headers["command"] += f'{name}="{var}" and '
        get_headers["command"] = get_headers["command"].rsplit(" and ", 1)[0]
    get_headers["command"] += " bring [*][id]"

    publish_headers = {
        "command": "blockchain insert where policy=!new_policy and local=true and master=!ledger_conn",
        "User-Agent": "Anylog/1.23"
    }

    response = conn.get_data(headers=get_headers)
    index = 0
    while not response or response == "[]":
        if index > 0:
            raise ConnectionError(f"Failed to publish policy against {conn.url}")
        new_policy = f"<new_policy={json.dumps(policy)}>"
        conn.publish_data(headers=publish_headers, payload=new_policy, method="POST")
        response = conn.get_data(headers=get_headers)
        index += 1

    return response


def declare_msg_client(conn:RestClient, broker:str, port:int, topics:str|list, is_rest:bool=True):
    # --- To review ---#
    is_topics = False
    if not isinstance(topics, list):
        topics = topics.split(',')

    for topic in topics:
        msg_topic = topic.split('name=', 1)[-1].split('and', 1)[0].strip()
        check_msg_client = {
            "command": f"get msg client where topic={msg_topic}",
            "User-Agent": "AnyLog/1.23"
        }
        response = conn.get_data(headers=check_msg_client)
        if not (response.strip() in ["No message client subscriptions", "No such client subscription"]):
            is_topics = True
            if len(topics) > 1:
                print(f"Topic {msg_topic} already defined, cannot define `msg client` for provided topics")

    if not is_topics:
        declare_msg_client_header = {
            "command": f"run msg client where broker={broker} and log=false",
            "User-Agent": "AnyLog/1.23"
        }
        for topic in topics:
            declare_msg_client_header["command"] += f" and topic={topic}"


        if broker not in ["rest", "local"] and port:
            declare_msg_client_header["command"] += f" and port={port}"
        if broker  == "rest" or is_rest is True:
            declare_msg_client_header["command"] += f" and user-agent=anylog"

        conn.publish_data(headers=declare_msg_client_header, payload=None, method="POST")
